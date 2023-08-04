import argparse

import pandas as pd
from utils.symbols import fileNames, folderNames, rulesExcelSymbols, getKaleConfigurationFolderName, USER_ITEM_FOLDER_NAME, USER_ITEM_PROP_FOLDER_NAME, DATASET_FOLDER_NAME_KEY, MAX_AD_FLAG, M_D_FLAG, DIMS_FLAG, M_GE_FLAG, M_GR_FLAG, SKIP_FLAG, TOP_K_FLAG, WEIGHT_FLAG, LIKE_ONLY_FLAG, ITERATIONS_FLAG, MINI_BATCH_FLAG, MIN_BODY_SIZE_FLAG, MIN_HEAD_COVERAGE_FLAG, WITH_ITEM_PROPERTIES_FLAG, MIN_PCA_BODY_SIZE_FLAG, MIN_PCA_CONFIDENCE_FLAG, MIN_STD_CONFIDENCE_FLAG, MIN_POSITIVE_EXAMPLES_FLAG, ALL_ITEMS_FLAG, CUTOFF_FLAG
from utils.common import loadJsonFileFromUtilsFolder

class _BaseSettings:
    def _extract(self, args: dict, flag: str):
        value = args[flag]
        print("%-20s%-12s" % (flag, value))
        return args[flag]

class AmieSettings(_BaseSettings):
    maxad: int

    def __init__(self, args: dict) -> None:
        self.maxad = self._extract(args, MAX_AD_FLAG)

    def getMaxAdFolderName(self):
        return f"{folderNames.MAX_AD_PREFIX}{self.maxad}"

    def areValid(self):
        return self.maxad is not None

class KaleSettings(_BaseSettings):
    dims: list
    mini_batch: int
    m_d: float
    m_gE: float
    m_gR:float
    iterations: int
    skip: int
    m_weight: float
    useItemProperties: bool

    userItemFolderName: str
    itemPropertiesFolderName: str

    def __init__(self, args: dict):
        self.dims = self._extract(args, DIMS_FLAG)
        self.mini_batch = self._extract(args, MINI_BATCH_FLAG)
        self.m_d = self._extract(args, M_D_FLAG)
        self.m_gE = self._extract(args, M_GE_FLAG)
        self.m_gR = self._extract(args, M_GR_FLAG)
        self.iterations = self._extract(args, ITERATIONS_FLAG)
        self.skip = self._extract(args, SKIP_FLAG)
        self.m_weight = self._extract(args, WEIGHT_FLAG)
        self.useItemProperties = self._extract(args, WITH_ITEM_PROPERTIES_FLAG)

        if self.useItemProperties:
            self.userItemFolderName = USER_ITEM_PROP_FOLDER_NAME
            self.itemPropertiesFolderName = folderNames.WITH_PROPS
        else:
            self.userItemFolderName = USER_ITEM_FOLDER_NAME
            self.itemPropertiesFolderName = folderNames.NO_PROPS

    def getConfigurationFolderName(self):
        return getKaleConfigurationFolderName(self.m_d, self.m_gE, self.m_gR, self.m_weight, self.mini_batch, self.iterations, self.skip)

class KaleTripSettings(KaleSettings):
    pass

class KaleJointSettings(KaleSettings):
    m_weight: float

class RulesFilter(_BaseSettings):
    minStdConfidence: float
    minHeadCoverage: float
    minPositiveExamples: int
    minPcaConfidence: float
    minBodySize: int
    minPcaBodySize: int
    #minFunctionalVariable: int TODO
    likesOnly: bool

    def __init__(self, args: dict) -> None:
        self.minPcaConfidence = self._extract(args, MIN_PCA_BODY_SIZE_FLAG)
        self.minHeadCoverage = self._extract(args, MIN_HEAD_COVERAGE_FLAG)
        self.minBodySize = self._extract(args, MIN_BODY_SIZE_FLAG)
        #self.minFunctionalVariable = self.__extract(args, MIN_FUNCTIONAL_VARIABLE) TODO
        self.minPcaBodySize = self._extract(args, MIN_PCA_BODY_SIZE_FLAG)
        self.minPositiveExamples = self._extract(args, MIN_POSITIVE_EXAMPLES_FLAG)
        self.minStdConfidence = self._extract(args, MIN_STD_CONFIDENCE_FLAG)
        self.likesOnly = self._extract(args, LIKE_ONLY_FLAG)

    def getSubsetName(self):
        SUBSET_NAME = []
        sep: str = rulesExcelSymbols.SEPARATOR_SHEET_NAME

        if self.likesOnly:
            SUBSET_NAME.append(rulesExcelSymbols.LIKES_ONLY_SHEET_NAME)
        else:
            SUBSET_NAME.append(rulesExcelSymbols.ALL_SHEET_NAME)

        def f(parameter, label: str):
            nonlocal SUBSET_NAME
            if parameter > 0:
                SUBSET_NAME.append(label.lower().replace(" ", sep))
                SUBSET_NAME.append(rulesExcelSymbols.OVER_INFIX_SHEET_NAME)
                SUBSET_NAME.append(f"{parameter}")

        f(self.minStdConfidence, rulesExcelSymbols.STD_CONFIDENCE_COLUMN_LABEL)
        f(self.minPositiveExamples, rulesExcelSymbols.POSITIVE_EXAMPLES_COLUMN_LABEL)
        f(self.minHeadCoverage, rulesExcelSymbols.HEAD_COVERAGE_COLUMN_LABEL)
        f(self.minPcaConfidence, rulesExcelSymbols.PCA_CONFIDENCE_COLUMN_LABEL)
        f(self.minBodySize, rulesExcelSymbols.BODY_SIZE_COLUMN_LABEL)
        f(self.minPcaBodySize, rulesExcelSymbols.PCA_BODY_SIZE_COLUMN_LABEL)
        
        return sep.join(SUBSET_NAME)

    def filter(self, rules: pd.DataFrame) -> pd.DataFrame:
        subset = rules[(rules[rulesExcelSymbols.STD_CONFIDENCE_COLUMN_LABEL] > self.minStdConfidence) & (rules[rulesExcelSymbols.HEAD_COVERAGE_COLUMN_LABEL] > self.minHeadCoverage) & (rules[rulesExcelSymbols.POSITIVE_EXAMPLES_COLUMN_LABEL] > self.minPositiveExamples) & (rules[rulesExcelSymbols.PCA_CONFIDENCE_COLUMN_LABEL] > self.minPcaConfidence) & (rules[rulesExcelSymbols.BODY_SIZE_COLUMN_LABEL] > self.minBodySize) & (rules[rulesExcelSymbols.PCA_BODY_SIZE_COLUMN_LABEL] > self.minPcaBodySize)]

        if self.likesOnly:
            return subset[subset[rulesExcelSymbols.RULE_COLUMN_LABEL].map(lambda row: row.split("=>")[-1].find(f" {rulesExcelSymbols.LIKE_RELATIONSHIP_LABEL} ")) != -1]
        else:
            return subset

class AmarSettings(_BaseSettings):
    topK: list
    allItems: bool

    def __init__(self, args: dict):
        self.topK = self._extract(args, TOP_K_FLAG)
        self.allItems = self._extract(args, ALL_ITEMS_FLAG)

class ElliotSettings(_BaseSettings):
    cutoff: list

    def __init__(self, args: dict):
        self.cutoff = self._extract(args, CUTOFF_FLAG)

def _loadDefaultValues(fileName: str):
    return loadJsonFileFromUtilsFolder(folderNames.DEFAULT_VALUES, fileName, "default values")

class Arguments:
    __parser: argparse.ArgumentParser

    def __init__(self) -> None:
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument(DATASET_FOLDER_NAME_KEY, type=str, help="dataset folder name inside pipeline/datasets")

    def __addArgument(self, defaultValues: dict, flag: str, expectedType: type, helpMessage: str, nargsValue: str = "?"):
        if (flag in defaultValues) and (defaultValues[flag] is not None):
            self.__parser.add_argument(f"--{flag}", type=expectedType, default=defaultValues[flag], nargs=nargsValue, help=helpMessage)
        else:
            self.__parser.add_argument(f"--{flag}", type=expectedType, required=True, help=helpMessage, nargs=nargsValue)
        
    def addAmieSettingsArguments(self):
        amieSettingsDefault = _loadDefaultValues(fileNames.AMIE_SETTINGS)
        self.__addArgument(amieSettingsDefault, MAX_AD_FLAG, int, "the maximum number of atoms per rule")

    def addAmieSettingsOptionalArguments(self):
        self.__parser.add_argument(f"--{MAX_AD_FLAG}", type=int, help="the maximum number of atoms per rule")

    def addRulesFilterArguments(self):
        rulesFilterDefault = _loadDefaultValues(fileNames.RULES_FILTER)
        
        self.__addArgument(rulesFilterDefault, MIN_STD_CONFIDENCE_FLAG, float, "minimum standard confidence per rule")
        self.__addArgument(rulesFilterDefault, MIN_HEAD_COVERAGE_FLAG, float, "minimum head coverage per rule")
        self.__addArgument(rulesFilterDefault, MIN_POSITIVE_EXAMPLES_FLAG, int, "minimum amount of positive examples per rule")
        self.__addArgument(rulesFilterDefault, MIN_PCA_CONFIDENCE_FLAG, float, "minimum PCA confidence per rule")
        self.__addArgument(rulesFilterDefault, MIN_BODY_SIZE_FLAG, int, "")
        self.__addArgument(rulesFilterDefault, MIN_PCA_BODY_SIZE_FLAG, int, "")
        #self.__addArgument(rulesFilterDefault, MIN_FUNCTIONAL_VARIABLE_FLAG, int, "")
        
        self.__parser.add_argument(f"--{LIKE_ONLY_FLAG}", action="store_true", help="Whether to consider only those rules which head includes a like relationship.")

    def addKaleSettingsArguments(self):
        kaleSettingsDefault = _loadDefaultValues(fileNames.KALE_SETTINGS)

        self.__addArgument(kaleSettingsDefault, DIMS_FLAG, int, "list of the dimensions of the embeddings to learn", "+")
        self.__addArgument(kaleSettingsDefault, M_D_FLAG, float, "")
        self.__addArgument(kaleSettingsDefault, M_GE_FLAG, float, "")
        self.__addArgument(kaleSettingsDefault, M_GR_FLAG, float, "")
        self.__addArgument(kaleSettingsDefault, ITERATIONS_FLAG, int, "amount of iterations to execute")
        self.__addArgument(kaleSettingsDefault, SKIP_FLAG, int, "")
        self.__addArgument(kaleSettingsDefault, WEIGHT_FLAG, float, "")
        self.__addArgument(kaleSettingsDefault, MINI_BATCH_FLAG, int, "")

        self.__parser.add_argument(f"--{WITH_ITEM_PROPERTIES_FLAG}", action="store_true", help="Whether to use triples with other relationships besides 'like' and 'dislike'.")

    def addAmarSettingsArguments(self):
        amarSettingsDefault = _loadDefaultValues(fileNames.AMAR_SETTINGS)

        self.__addArgument(amarSettingsDefault, TOP_K_FLAG, int, "list of top Ks", "+")
        self.__parser.add_argument(f"--{ALL_ITEMS_FLAG}", action="store_true", help="Whether to use triples from the train set instead of those from the test set for the predictions.")

    def addElliotSettingsArguments(self):
        #amarSettingsDefault = _loadDefaultValues(fileNames.ELLIOT_ARG_SETTINGS)
        self.__parser.add_argument(f"--{CUTOFF_FLAG}", type=int, help="", nargs="+")

    def parse(self):
        args = vars(self.__parser.parse_args())
        return (args[DATASET_FOLDER_NAME_KEY], args)