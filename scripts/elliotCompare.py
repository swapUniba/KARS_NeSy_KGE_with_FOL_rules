import os
from pathlib import Path

import yaml
from elliot.run import run_experiment
from utils.arguments import Arguments
from utils.paths import  getUserItemAmarAllItemsFilePath, folderNames, fileNames, getComparisonsElliotFolderPath, getComparisonsElliotSettingsFilePath, getComparisonsPredictionsFolderPath, getNoRulesEmbeddingsFolderPath, getComparisonsFolderPath, getUserItemAmarTestLikeOnlyFilePath, getUserItemAmarTrainFilePath, getWithRulesFolderPath
from shutil import copyfile

# TODO: Considerare tutte le cartelle "maxad", non solo la prima individuata
# Nel tirocinio si è eseguito AMIE solo una volta per dataset, quindi la prima cartella "maxad" che si individua è anche l'unica esistente.

# TODO: sinceramente, questo script sarebbe completamente da ripensare, ma per il momento funziona

def exploreEmbeddingsFolder(datasetFolderName: str, embeddingsFolderPath: Path, rulesSubsetName: str):
    folders = os.listdir(embeddingsFolderPath)

    for itemPropConfig in folders:
        fileName = f"{itemPropConfig}+{rulesSubsetName}.tsv"

        embeddingsPath = Path(embeddingsFolderPath, itemPropConfig)

        for embeddingConfig in os.listdir(embeddingsPath):
            dimensionsPath = Path(embeddingsPath, embeddingConfig)
            
            for dimension in os.listdir(dimensionsPath):
                predictionsPath = Path(dimensionsPath, dimension, folderNames.PREDICTIONS)
                
                for top in os.listdir(predictionsPath):
                    if "_allItems" in top:
                        continue

                    predictionsFile = Path(predictionsPath, top, fileNames.PREDICTIONS_1)
                    
                    if not os.path.exists(predictionsFile):
                        print(f"{predictionsFile} does not exist")
                        continue
                    
                    comparisonsPredictionsFolderPath = getComparisonsPredictionsFolderPath(datasetFolderName, dimension, top)
                    
                    if not os.path.exists(comparisonsPredictionsFolderPath):
                        os.makedirs(comparisonsPredictionsFolderPath)
                    
                    copiedFilePath = Path(comparisonsPredictionsFolderPath, fileName)

                    if os.path.exists(copiedFilePath):
                        print(f"{copiedFilePath} already exists")
                        continue

                    copyfile(predictionsFile, copiedFilePath)
                    print(f"{predictionsFile}\ncopied to\n{copiedFilePath}\n")

def noRules(datasetFolderName: str):
    embeddingsFolderPath = getNoRulesEmbeddingsFolderPath(datasetFolderName)

    if not os.path.exists(embeddingsFolderPath):
        print(f"Path {embeddingsFolderPath} not found.")
        return

    exploreEmbeddingsFolder(datasetFolderName, embeddingsFolderPath, None)

def withRules(datasetFolderName: str):
    mainPath = getWithRulesFolderPath(datasetFolderName)

    if not os.path.exists(mainPath):
        print(f"Path {mainPath} not found.")
        return

    folders = os.listdir(mainPath)

    for maxad in folders:
        maxAdFolder = Path(mainPath, maxad)

        for rulesSubsetName in os.listdir(maxAdFolder):
            embeddingsFolderFolder = Path(maxAdFolder, rulesSubsetName, folderNames.EMBEDDINGS)

            if not os.path.exists(embeddingsFolderFolder):
                continue

            exploreEmbeddingsFolder(datasetFolderName, embeddingsFolderFolder, rulesSubsetName)

if __name__ == "__main__":
    parser = Arguments()
    (datasetFolderName, args) = parser.parse()
    
    comparisonsFolderPath = getComparisonsFolderPath(datasetFolderName)

    if not os.path.exists(comparisonsFolderPath):
        os.makedirs(comparisonsFolderPath)

    noRules(datasetFolderName)
    withRules(datasetFolderName)

    amarTrainPath = getUserItemAmarTrainFilePath(datasetFolderName)

    for dimension in os.listdir(comparisonsFolderPath):
        dimensionFolder = Path(comparisonsFolderPath, dimension)

        for top in os.listdir(dimensionFolder):
            tokens = top.split("_")
            
            if(len(tokens) == 2):
                continue
                # amarTestPath = getUserItemAmarAllItemsFilePath(datasetFolderName)
            else:
                amarTestPath = getUserItemAmarTestLikeOnlyFilePath(datasetFolderName)

            predictionsFolder = getComparisonsPredictionsFolderPath(datasetFolderName, dimension, top)
            elliotFolder = getComparisonsElliotFolderPath(datasetFolderName, dimension, top)

            if not os.path.exists(elliotFolder):
                os.makedirs(elliotFolder)
                print(f"New path: {elliotFolder}")

            config = {
                "experiment": {
                    "gpu": 1,
                    "path_output_rec_performance": str(elliotFolder),
                    "dataset": top,
                    "data_config": {
                        "strategy": "fixed",
                        "train_path": str(amarTrainPath),
                        "test_path": str(amarTestPath),
                    },
                    "evaluation": {
                        "simple_metrics": ["MAP", "Precision", "MAR", "Recall", "F1", "nDCG", "Gini", "ItemCoverage", "EFD", "EPC"],
                        "paired_ttest": True,
                        "wilcoxon_test": True
                    },
                    "models": {
                        "RecommendationFolder": {
                            "folder": str(predictionsFolder)
                        }
                    },
                    "top_k": int(tokens[0].split("top")[1])
                }
            }

            elliotConfigFilePath = getComparisonsElliotSettingsFilePath(datasetFolderName, dimension, top)

            with open(elliotConfigFilePath, "w") as f:
                yaml.dump(config, f)

            run_experiment(elliotConfigFilePath)