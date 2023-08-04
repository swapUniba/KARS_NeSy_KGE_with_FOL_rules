import os
from utils.arguments import AmieSettings, Arguments, KaleSettings, RulesFilter, AmarSettings, ElliotSettings
from utils.paths import getPredictions1FilePath, getTopPredictionsFolderPath
import pandas as pd
from runElliot import runElliot
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension

def f(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, elliotSettings: ElliotSettings, dimension: int, amieSettings: AmieSettings):
    k = amarSettings.topK[0]

    predictions = getPredictions1FilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, k)
    df = pd.read_csv(predictions, sep='\t', header=None)

    for cutoff in elliotSettings.cutoff:
        folderPath = getTopPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, cutoff)
        
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
            print(f"New path: {folderPath}")
        
        grouped = df.groupby(0)
        limited = grouped.apply(lambda x: x[:cutoff])
        limited.reset_index(drop=True, inplace=True)

        filePath = getPredictions1FilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, cutoff)
        limited.to_csv(filePath, sep='\t', index=False, header=False)
        
        print(f"New file: {filePath}")

    del df

    topK = amarSettings.topK
    amarSettings.topK = elliotSettings.cutoff
    runElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings)
    amarSettings.topK = topK
    
if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()
    parser.addAmarSettingsArguments()
    parser.addElliotSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    kaleSettings = KaleSettings(args)
    rulesFilter = RulesFilter(args)
    amarSettings = AmarSettings(args)
    elliotSettings = ElliotSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: f(datasetFolderName, rulesFilter, kaleSettings, amarSettings, elliotSettings, dim, amieSettings))