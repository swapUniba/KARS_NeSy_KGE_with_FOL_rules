import os
from pathlib import Path
import subprocess
import pandas as pd
from utils.arguments import AmieSettings, KaleSettings, RulesFilter, Arguments
from utils.exceptions import KaleException
from utils.paths import getEntityIDFilePath, getRelationIDFilePath, KALE_TRIP_PROGRAM_FILE_PATH, getMatrixEFilePath, getMatrixRFilePath, getKALELogsFilePath, getTestFilePath, getTrainFilePath, getValidFilePath, getGroundingsFilePath, getEmbeddingsConfigurationDimensionFolderPath, KALE_JOINT_PROGRAM_FILE_PATH
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension

def _countRows(path: Path):
    try:
        df = pd.read_csv(path, sep="\t", header=None)
        dfRowsAmount = len(df)
        return str(dfRowsAmount)
    except (FileNotFoundError, ValueError) as e:
        raise KaleException(f"Could not count the rows of file {path}", e)

def runKale(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int, amieSettings: AmieSettings):
    train = getTrainFilePath(datasetFolderName, kaleSettings)
    valid = getValidFilePath(datasetFolderName, kaleSettings)
    test = getTestFilePath(datasetFolderName, kaleSettings)
    
    inputFiles = [train, valid, test]

    matrixE = getMatrixEFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
    matrixR = getMatrixRFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
    logs = getKALELogsFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)

    outputFiles = [matrixE, matrixR, logs]

    entitiesCount = _countRows(getEntityIDFilePath(datasetFolderName, kaleSettings))
    relationsCount = _countRows(getRelationIDFilePath(datasetFolderName, kaleSettings))

    params = [entitiesCount, relationsCount, str(dimension), str(kaleSettings.mini_batch), str(kaleSettings.m_d), str(kaleSettings.m_gE), str(kaleSettings.m_gR), str(kaleSettings.iterations), str(kaleSettings.skip)]

    if amieSettings.areValid():
        JAR_FILE = KALE_JOINT_PROGRAM_FILE_PATH
        groundings = getGroundingsFilePath(datasetFolderName, amieSettings, rulesFilter)
        inputFiles.append(groundings)
        params.append(str(kaleSettings.m_weight))
    else:
        JAR_FILE = KALE_TRIP_PROGRAM_FILE_PATH
        
    embeddingDimensionPath = getEmbeddingsConfigurationDimensionFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
    
    if not os.path.exists(embeddingDimensionPath):
        os.makedirs(embeddingDimensionPath)
        print(f"Created path: {embeddingDimensionPath}")

    try:
        subprocess.check_call(["java", "-jar", JAR_FILE, *inputFiles, *outputFiles, *params])
    except subprocess.SubprocessError as e:
        raise KaleException("Java process failed to execute correctly", e)
    
    kaleLogsPath = getKALELogsFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)

    fileExists = os.path.exists(kaleLogsPath)

    if fileExists:
        fileIsEmpty = os.path.getsize(kaleLogsPath) == 0     
        if not fileIsEmpty:
            f = open(kaleLogsPath, "r")
            line = f.readlines()[-3]
            f.close()
            if line == f"Complete iteration #{kaleSettings.iterations}:\n":
                return

    raise KaleException("Java process did not output the expected results", Exception("read above"))

if __name__ == "__main__":
    parser = Arguments()
    
    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    rulesFilter = RulesFilter(args)
    kaleSettings = KaleSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: runKale(datasetFolderName, rulesFilter, kaleSettings, dim, amieSettings))