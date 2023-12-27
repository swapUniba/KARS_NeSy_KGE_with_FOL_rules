import os
from utils.arguments import AmieSettings, Arguments, KaleSettings, RulesFilter, AmarSettings
from elliot.run import run_experiment
from utils.exceptions import ElliotException
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension
from utils.paths import getUserItemAmarAllItemsFilePath, getUserItemAmarTestLikeOnlyFilePath, getUserItemAmarTrainFilePath, getTopPredictionsFolderPath, getElliotOutputFolderPath, getElliotSettingsFilePath
import yaml

def runElliot(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int,amieSettings: AmieSettings):
    amarTrainPath = getUserItemAmarTrainFilePath(datasetFolderName)

    if amarSettings.allItems:
        amarTestPath = getUserItemAmarAllItemsFilePath(datasetFolderName)
    else:
        amarTestPath = getUserItemAmarTestLikeOnlyFilePath(datasetFolderName)
        
    for k in amarSettings.topK:
        try:
            topPredictionsFolderPath = getTopPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, k)

            elliotOutputPath = getElliotOutputFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, k)
            
            if not os.path.exists(elliotOutputPath):
                os.makedirs(elliotOutputPath)
                print(f"New path: {elliotOutputPath}")

            config = {
                "experiment": {
                    "gpu": 1,
                    "path_output_rec_performance": str(elliotOutputPath),
                    "dataset": datasetFolderName,
                    "data_config": {
                        "strategy": "fixed",
                        "train_path": str(amarTrainPath),
                        "test_path": str(amarTestPath),
                    },
                    "evaluation": {
                        "simple_metrics": ["MAP", "Precision", "MAR", "Recall", "F1", "nDCG", "Gini", "UserCoverageAtN", "EFD", "EPC"],
                        "paired_ttest": True,
                        "wilcoxon_test": True
                    },
                    "models": {
                        "RecommendationFolder": {
                            "folder": str(topPredictionsFolderPath)
                        }
                    },
                    "top_k": k
                }
            }

            elliotConfigFilePath = getElliotSettingsFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, k)

            with open(elliotConfigFilePath, "w") as f:
                yaml.dump(config, f)

            run_experiment(elliotConfigFilePath)
        except Exception as e:
            raise ElliotException(k, "a generic error occurred", e)

if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()
    parser.addAmarSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    kaleSettings = KaleSettings(args)
    rulesFilter = RulesFilter(args)
    amarSettings = AmarSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: runElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dim, amieSettings))