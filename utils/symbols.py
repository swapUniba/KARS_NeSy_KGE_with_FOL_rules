from pathlib import Path
from types import SimpleNamespace
from utils.common import loadJsonFileFromUtilsFolder

SYMBOLS_FOLDER_NAME = "symbolicConstants"

def _loadSymbolsIntoNamespace(fileName: str) -> SimpleNamespace:
    return loadJsonFileFromUtilsFolder(SYMBOLS_FOLDER_NAME, fileName, "symbols", lambda d: SimpleNamespace(**d))

FILES_FILE_NAME = "files.json"
FOLDER_FILE_NAME = "folders.json"
RULES_EXCEL_SYMBOLS_FILE_NAME = "rules_excel_file.json"

fileNames = _loadSymbolsIntoNamespace(FILES_FILE_NAME)
folderNames = _loadSymbolsIntoNamespace(FOLDER_FILE_NAME)
rulesExcelSymbols = _loadSymbolsIntoNamespace(RULES_EXCEL_SYMBOLS_FILE_NAME)

USER_ITEM_RELATIONSHIPS_LABELS = [] # "like" e "dislike" sono esclusi. Poiché fondamentali, si danno per scontati: in questa lista ci sono le ALTRE relazioni user-item

DATASET_FOLDER_NAME_KEY = "datasetFolderName"

MAX_AD_FLAG = "maxad"

DIMS_FLAG = "dims"
MINI_BATCH_FLAG = "miniBatch"
M_D_FLAG = "m_d"
M_GE_FLAG = "m_gE"
M_GR_FLAG = "m_gR"
ITERATIONS_FLAG = "iterations"
SKIP_FLAG = "skip"
WEIGHT_FLAG = "weight"
WITH_ITEM_PROPERTIES_FLAG = "itemProperties"

MINI_BATCH_FLAG_SHORT = "mb"
M_D_FLAG_SHORT = "d"
M_GE_FLAG_SHORT = "ge"
M_GR_FLAG_SHORT = "gr"
ITERATIONS_FLAG_SHORT = "i"
SKIP_FLAG_SHORT = "s"
WEIGHT_FLAG_SHORT = "w"

MIN_STD_CONFIDENCE_FLAG = "minStdConfidence"
MIN_HEAD_COVERAGE_FLAG = "minHeadCoverage"
MIN_POSITIVE_EXAMPLES_FLAG = "minPositiveExamples"
MIN_PCA_CONFIDENCE_FLAG = "minPcaConfidence"
MIN_BODY_SIZE_FLAG = "minBodySize"
MIN_PCA_BODY_SIZE_FLAG = "minPcaBodySize"
MIN_FUNCTIONAL_VARIABLE_FLAG = "minFunctionalVariable"
LIKE_ONLY_FLAG = "likeInHead"

TOP_K_FLAG = "top"
ALL_ITEMS_FLAG = "allItems"

CUTOFF_FLAG = "cutoff"

#TODO ^mettere in dei file JSON anche tutti questi simboli (e pure messaggi "help="?)

def getKaleDimensionFolderName(dimension: int):
    return f"{folderNames.DIM_PREFIX}{dimension}"

def getAmarTopKFolderName(k: int):
    return f"{folderNames.TOP_PREFIX}{k}"

def getKaleConfigurationFolderName(m_d: float, m_gE: float, m_gR: float, m_weight: float, mini_batch: int, iterations: int, skip: int):
    sep: str = folderNames.KALE_CONFIGURATION_INFIX
    labels = [f"{M_D_FLAG_SHORT}{m_d}", f"{M_GE_FLAG_SHORT}{m_gE}", f"{M_GR_FLAG_SHORT}{m_gR}", f"{WEIGHT_FLAG_SHORT}{m_weight}", f"{MINI_BATCH_FLAG_SHORT}{mini_batch}", f"{ITERATIONS_FLAG_SHORT}{iterations}", f"{SKIP_FLAG_SHORT}{skip}"]
    return sep.join(labels)

USER_ITEM_PROP_FOLDER_NAME = folderNames.USER_ITEM_PROP
USER_ITEM_FOLDER_NAME = folderNames.USER_ITEM