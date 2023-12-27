import os
from pathlib import Path

from utils.arguments import AmieSettings, KaleSettings, RulesFilter, AmarSettings
from utils.symbols import getAmarTopKFolderName, getKaleDimensionFolderName, fileNames, folderNames, rulesExcelSymbols, USER_ITEM_FOLDER_NAME, USER_ITEM_PROP_FOLDER_NAME, ALL_ITEMS_FLAG
from utils.common import BASE_FOLDER_PATH, getUtilsFolderPath

def getJarsFolderPath(*argv):
    return getUtilsFolderPath(folderNames.JARS, *argv)

AMIE_INIT_FILE_PATH = getJarsFolderPath(fileNames.AMIE_INIT)
GROUND_ALL_RULES_FILE_PATH = getJarsFolderPath(fileNames.GROUND_ALL_RULES)
CONVERT_DATA_FORM_FILE_PATH = getJarsFolderPath(fileNames.CONVERT_DATA_FORM)
KALE_JOINT_PROGRAM_FILE_PATH = getJarsFolderPath(fileNames.KALE_JOINT_PROGRAM)
KALE_TRIP_PROGRAM_FILE_PATH = getJarsFolderPath(fileNames.KALE_TRIP_PROGRAM)

RELATIVE_ROOT_PATH = Path("..") # relative from BASE_FOLDER_PATH

ROOT_PATH = os.path.abspath(Path(BASE_FOLDER_PATH, RELATIVE_ROOT_PATH))

DATASETS_FOLDER_PATH = Path(ROOT_PATH, folderNames.DATASETS)

def getDatasetFolderPath(datasetFolderName: str, *argv):
    return Path(DATASETS_FOLDER_PATH, datasetFolderName, *argv)

def getUserItemPropFolderPath(datasetFolderName: str, *argv):
    folderName = USER_ITEM_PROP_FOLDER_NAME
    return getDatasetFolderPath(datasetFolderName, folderName, *argv)

def getUserItemFolderPath(datasetFolderName: str, *argv):
    folderName = USER_ITEM_FOLDER_NAME
    return getDatasetFolderPath(datasetFolderName, folderName, *argv)

def getUserItemPropAmarTrainFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.AMAR_TRAIN)

def getUserItemPropAmarTestFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.AMAR_TEST)

def getUserItemAmarAllItemsFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.AMAR_ALL_ITEMS)

def getUserItemAmarTrainFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.AMAR_TRAIN)

def getUserItemAmarTestFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.AMAR_TEST)

def getUserItemAmarTestLikeOnlyFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.AMAR_TEST_LIKE_ONLY)

def getUserItemPropKaleTrainFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.KALE_TRAIN)

def getUserItemPropKaleValidFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.KALE_VALID)

def getUserItemPropKaleTestFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.KALE_TEST)

def getUserItemKaleTrainFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.KALE_TRAIN)

def getUserItemKaleValidFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.KALE_VALID)

def getUserItemKaleTestFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.KALE_TEST)

def getWithRulesFolderPath(datasetFolderName: str, *argv):
    return getDatasetFolderPath(datasetFolderName, folderNames.WITH_RULES, *argv)

def getMaxAdFolderPath(datasetFolderName: str, amieSettings: AmieSettings, *argv):
    folderName = amieSettings.getMaxAdFolderName()
    return getWithRulesFolderPath(datasetFolderName, folderName, *argv)

def getRulesExcelFilePath(datasetFolderName: str, amieSettings: AmieSettings):
    return getMaxAdFolderPath(datasetFolderName, amieSettings, fileNames.RULES_EXCEL)

def getRulesRulesFilePath(datasetFolderName: str, amieSettings: AmieSettings):
    return getMaxAdFolderPath(datasetFolderName, amieSettings, fileNames.RULES_RULES)

def getUserItemPropRelationIDFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.RELATION_ID)

def getUserItemRelationIDFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.RELATION_ID)

def getUserItemPropEntityIDFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.ENTITY_ID)

def getUserItemFolderPathGeneric(datasetFolderName: str, kaleSettings: KaleSettings, *argv):
    return getDatasetFolderPath(datasetFolderName, kaleSettings.userItemFolderName, *argv)

def getEntityIDFilePath(datasetFolderName: str, kaleSettings: KaleSettings):
    return getUserItemFolderPathGeneric(datasetFolderName, kaleSettings, fileNames.ENTITY_ID)

def getRelationIDFilePath(datasetFolderName: str, kaleSettings: KaleSettings):
    return getUserItemFolderPathGeneric(datasetFolderName, kaleSettings, fileNames.RELATION_ID)

def getValidFilePath(datasetFolderName: str, kaleSettings: KaleSettings):
    return getUserItemFolderPathGeneric(datasetFolderName, kaleSettings, fileNames.VALID)

def getTrainFilePath(datasetFolderName: str, kaleSettings: KaleSettings):
    return getUserItemFolderPathGeneric(datasetFolderName, kaleSettings, fileNames.TRAIN)

def getTestFilePath(datasetFolderName: str, kaleSettings: KaleSettings):
    return getUserItemFolderPathGeneric(datasetFolderName, kaleSettings, fileNames.TEST)

def getUserItemEntityIDFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.ENTITY_ID)

def getUserItemPropTestFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.TEST)

def getUserItemTestFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.TEST)

def getUserItemPropValidFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.VALID)

def getUserItemValidFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.VALID)

def getUserItemPropTrainFilePath(datasetFolderName: str):
    return getUserItemPropFolderPath(datasetFolderName, fileNames.TRAIN)

def getUserItemTrainFilePath(datasetFolderName: str):
    return getUserItemFolderPath(datasetFolderName, fileNames.TRAIN)

def _getRulesSubsetFolderPath(datasetFolderName: str, amieSettings: AmieSettings, subsetName: str, *argv):
    return getMaxAdFolderPath(datasetFolderName, amieSettings, subsetName, *argv)

def getRulesSubsetFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, *argv):
    subsetName = rulesFilter.getSubsetName()
    return _getRulesSubsetFolderPath(datasetFolderName, amieSettings, subsetName, *argv)

def getRulesSubsetAllFolderPath(datasetFolderName: str, amieSettings: AmieSettings, *argv):
    return _getRulesSubsetFolderPath(datasetFolderName, amieSettings, rulesExcelSymbols.ALL_SHEET_NAME, *argv)

def getGroundingsFilePath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter):
    return getRulesSubsetFolderPath(datasetFolderName, amieSettings, rulesFilter, fileNames.GROUNDINGS)

def getAllGroundingsFilePath(datasetFolderName: str, amieSettings: AmieSettings):
    return getRulesSubsetAllFolderPath(datasetFolderName, amieSettings, fileNames.GROUNDINGS)

def getAMIEOutputFilePath(datasetFolderName: str, amieSettings: AmieSettings):
    return getMaxAdFolderPath(datasetFolderName, amieSettings, fileNames.AMIE_OUTPUT)

def getMappingRelationsFilePath(datasetFolderName: str):
    return getDatasetFolderPath(datasetFolderName, fileNames.MAPPING_RELATIONS)

def getMappingUsersFilePath(datasetFolderName: str):
    return getDatasetFolderPath(datasetFolderName, fileNames.MAPPING_USERS)

def getMappingItemsFilePath(datasetFolderName: str):
    return getDatasetFolderPath(datasetFolderName, fileNames.MAPPING_ITEMS)

def getMappingPropsFilePath(datasetFolderName: str):
    return getDatasetFolderPath(datasetFolderName, fileNames.MAPPING_PROPS)

def getNoRulesFolderPath(datasetFolderName: str, *argv):
    return getDatasetFolderPath(datasetFolderName, folderNames.NO_RULES, *argv)

def getNoRulesEmbeddingsFolderPath(datasetFolderName: str, *argv):
    return getNoRulesFolderPath(datasetFolderName, folderNames.EMBEDDINGS, *argv)

def getEmbeddingsFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, *argv):
    if amieSettings.areValid():
        return getRulesSubsetFolderPath(datasetFolderName, amieSettings, rulesFilter, folderNames.EMBEDDINGS, *argv)

    return getNoRulesEmbeddingsFolderPath(datasetFolderName, *argv)

def getItemPropertiesFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, *argv):
    return getEmbeddingsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings.itemPropertiesFolderName, *argv)

def getEmbeddingsConfigurationFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, *argv):    
    kaleConfigName = kaleSettings.getConfigurationFolderName()
    return getItemPropertiesFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, kaleConfigName, *argv)

def getEmbeddingsConfigurationDimensionFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int, *argv):
    dimStr = getKaleDimensionFolderName(dimension)
    return getEmbeddingsConfigurationFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimStr, *argv)

def getMatrixEFilePath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int):
    return getEmbeddingsConfigurationDimensionFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, fileNames.ENTITY_MATRIX)

def getMatrixRFilePath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int):
    return getEmbeddingsConfigurationDimensionFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, fileNames.RELATION_MATRIX)

def getKALELogsFilePath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int):
    return getEmbeddingsConfigurationDimensionFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, fileNames.KALE_LOGS)

def getResultsFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int, *argv):
    return getEmbeddingsConfigurationDimensionFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, folderNames.RESULTS, *argv)

def getModelFilePath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int):
    return getResultsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, fileNames.MODEL)

def getPredictionsFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, dimension: int, *argv):
    return getEmbeddingsConfigurationDimensionFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, folderNames.PREDICTIONS, *argv)

def getTopPredictionsFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, topK: int, *argv):
    topKStr = getAmarTopKFolderName(topK)

    if amarSettings.allItems:
        topKStr += f"_{ALL_ITEMS_FLAG}"

    return getPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension, topKStr, *argv)

def getPredictions1FilePath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, topK: int):
    return getTopPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, topK, fileNames.PREDICTIONS_1)

def getElliotFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, topK: int, *argv):
    return getTopPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, topK, folderNames.ELLIOT, *argv)

def getElliotOutputFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, topK: int, *argv):
    return getElliotFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, topK, folderNames.ELLIOT_OUTPUT, *argv)

def getElliotResultsFolderPath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, topK: int, *argv):
    return getTopPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, topK, folderNames.ELLIOT_RESULTS, *argv)

def getElliotSettingsFilePath(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, topK: int):
    return getElliotFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, topK, fileNames.ELLIOT_SETTINGS)

def getComparisonsFolderPath(datasetFolderName: str, *argv):
    return getDatasetFolderPath(datasetFolderName, folderNames.COMPARISONS, *argv)

def getComparisonsPredictionsFolderPath(datasetFolderName: str, dim: str, top: str, *argv):
    return getComparisonsFolderPath(datasetFolderName, dim, top, folderNames.PREDICTIONS, *argv)

def getComparisonsElliotFolderPath(datasetFolderName: str, dim: str, top: str, *argv):
    return getComparisonsFolderPath(datasetFolderName, dim, top, folderNames.ELLIOT, *argv)

def getComparisonsElliotSettingsFilePath(datasetFolderName: str, dim: str, top: str):
    return getComparisonsFolderPath(datasetFolderName, dim, top, fileNames.ELLIOT_SETTINGS)