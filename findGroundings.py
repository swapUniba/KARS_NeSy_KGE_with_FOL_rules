import os
import pandas as pd
from utils.arguments import AmieSettings, Arguments, RulesFilter
from utils.paths import getRulesSubsetFolderPath, getAllGroundingsFilePath, getGroundingsFilePath, getRulesExcelFilePath, getUserItemPropRelationIDFilePath
from utils.symbols import rulesExcelSymbols
from utils.mappingRelations import replaceRelationshipLabelsWithIDs
import re

def findGroundings(datasetPath: str, amieSettings: AmieSettings, rulesFilter: RulesFilter):
    rulesExcelSheetName = rulesFilter.getSubsetName()
    
    if(rulesExcelSheetName == rulesExcelSymbols.ALL_SHEET_NAME):
        return

    rulesSubsetFolderPath = getRulesSubsetFolderPath(datasetPath, amieSettings, rulesFilter)
    
    if not os.path.exists(rulesSubsetFolderPath):
        os.makedirs(rulesSubsetFolderPath)
        print(f"New path: {rulesSubsetFolderPath}")

    print("Loading necessary files into memory...")

    INPUT_PATH = getRulesExcelFilePath(datasetPath, amieSettings)

    rules = pd.read_excel(INPUT_PATH, rulesExcelSheetName, usecols=[rulesExcelSymbols.RULE_COLUMN_LABEL], engine="odf")
    replaceRelationshipLabelsWithIDs(rules, datasetPath)

    matrixRowsToRelationIDsMap = pd.read_csv(getUserItemPropRelationIDFilePath(datasetPath), sep="\t", header=None)
    relationIDsToMatrixRowsMap = matrixRowsToRelationIDsMap[matrixRowsToRelationIDsMap.columns[::-1]]
    relationIDsToMatrixRowsMap = dict(relationIDsToMatrixRowsMap.values)

    groundings = pd.read_csv(getAllGroundingsFilePath(datasetPath, amieSettings), header=None)

    totalAmount = 0

    targetFilePath = getGroundingsFilePath(datasetPath, amieSettings, rulesFilter)

    f = open(targetFilePath, "w")
    f.close()

    print(f"\nNew file: {targetFilePath}\n")

    for i, row in rules.iterrows():
        print(f"Processing rule {i + 1} of {len(rules)}")
        print(f"Rule: {row[rulesExcelSymbols.RULE_COLUMN_LABEL]}")

        rule =  row[rulesExcelSymbols.RULE_COLUMN_LABEL].replace("?", "")
        rule = rule.replace("  ", " ")
        [body, head] = rule.split(" => ")
        atoms = re.findall("([a-z] \\d+ [a-z])", body)
        atoms.append(head)
        
        regex = []

        entities = {}
        entitiesCount = 0

        for atom in atoms:
            [e1, r, e2] = atom.split(" ")

            if e1 in entities:
                e1regex = fr"\{entities[e1]}"
            else:
                entitiesCount += 1
                entities[e1] = entitiesCount
                e1regex = r"(\d+)"

            if e2 in entities:
                e2regex = fr"\{entities[e2]}"
            else:
                entitiesCount += 1
                entities[e2] = entitiesCount
                e2regex = r"(\d+)"

            relationMatrixRow = relationIDsToMatrixRowsMap[int(r)]

            regex.append(fr"\({e1regex}\t{relationMatrixRow}\t{e2regex}\)")

        regex = r"\t".join(regex)

        res = groundings[groundings[0].str.fullmatch(regex)]

        resAmount = len(res)
        totalAmount += resAmount

        print(f"{resAmount} matching ground expressions found.")

        res.to_csv(targetFilePath, mode='a', header=False, index=False)

        print(f"{targetFilePath} updated.\n")

    print(f"Successfully terminated after {totalAmount} hits.")

if __name__ == "__main__":
    parser = Arguments()
    
    parser.addAmieSettingsArguments()
    parser.addRulesFilterArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    rulesFilter = RulesFilter(args)

    findGroundings(datasetFolderName, amieSettings, rulesFilter)