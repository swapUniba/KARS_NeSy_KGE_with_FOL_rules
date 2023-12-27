from utils.paths import getMappingRelationsFilePath
from utils.symbols import rulesExcelSymbols
import pandas as pd
import re

def _removeURLsFromLabelColumn(df: pd.DataFrame, columnIndex: int):
    def getSubStringAfterLastSlash(label: str):
        return label.split("/")[-1]

    df[columnIndex] = df[columnIndex].apply(getSubStringAfterLastSlash)

def _loadMappingRelations(datasetFolderName: str):
    mappingRelationsFilePath = getMappingRelationsFilePath(datasetFolderName)
    
    relationships = pd.read_csv(mappingRelationsFilePath, sep="\t", header=None)

    colCount = len(relationships.columns)

    expectedColCount = 2

    if colCount != expectedColCount:
        raise Exception(f"{mappingRelationsFilePath} should not have more than {expectedColCount} columns")

    try:
        column = 0
        _removeURLsFromLabelColumn(relationships, column)
    except AttributeError: # se nella prima colonna ci sono gli ID, non le label
        column = 1
        _removeURLsFromLabelColumn(relationships, column)

    return (relationships, column)

def _loadMappingRelationsAndSwapLabelColumnToExpectedIndex(datasetFolderName: str, expectedLabelColumn: int):
    (df, labelColumn) = _loadMappingRelations(datasetFolderName)

    if labelColumn == expectedLabelColumn:
        return df
    else:
        return df[df.columns[::-1]]

def getMappingRelationsIDsToLabels(datasetFolderName: str) -> dict:
    relationships = _loadMappingRelationsAndSwapLabelColumnToExpectedIndex(datasetFolderName, 1)
    return dict(relationships.values)

def getMappingRelationsLabelsToIDs(datasetFolderName: str) -> dict:
    relationships = _loadMappingRelationsAndSwapLabelColumnToExpectedIndex(datasetFolderName, 0)
    return dict(relationships.values)

def replaceRelationshipIDsWithLabels(rules: pd.DataFrame, datasetFolderName: str):
    relationships = getMappingRelationsIDsToLabels(datasetFolderName)

    def f(rule: str):
        strlist = re.split('(\\d+)', rule)
        strlist = list(map(lambda token: relationships[int(token)] if token.isdigit() else token, strlist))
        return "".join(strlist)

    rules[rulesExcelSymbols.RULE_COLUMN_LABEL] = rules[rulesExcelSymbols.RULE_COLUMN_LABEL].apply(f)

def replaceRelationshipLabelsWithIDs(rules: pd.DataFrame, datasetFolderName: str):
    relationships = getMappingRelationsLabelsToIDs(datasetFolderName)

    def f(rule: str):
        strlist = re.split(' (\\w+) ', rule)
        strlist = list(map(lambda token: f"{relationships[token]}" if token in relationships else token, strlist))
        return " ".join(strlist)

    rules[rulesExcelSymbols.RULE_COLUMN_LABEL] = rules[rulesExcelSymbols.RULE_COLUMN_LABEL].apply(f)