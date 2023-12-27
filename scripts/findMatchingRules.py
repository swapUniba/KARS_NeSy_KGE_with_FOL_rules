import pandas as pd
from utils.paths import getRulesExcelFilePath
from utils.symbols import rulesExcelSymbols
from utils.arguments import AmieSettings, RulesFilter, Arguments

def findMatchingRules(datasetPath: str, amieSettings: AmieSettings, rulesFilter: RulesFilter):
    SUBSET_NAME = rulesFilter.getSubsetName()

    if SUBSET_NAME == rulesExcelSymbols.ALL_SHEET_NAME:
        return
    
    INPUT_PATH = getRulesExcelFilePath(datasetPath, amieSettings)

    sheets = {}

    for sheetName in pd.ExcelFile(INPUT_PATH).sheet_names:
        sheets[sheetName] = pd.read_excel(INPUT_PATH, sheetName, engine="odf")

    sheets[SUBSET_NAME] = rulesFilter.filter(sheets[rulesExcelSymbols.ALL_SHEET_NAME])

    with pd.ExcelWriter(INPUT_PATH, mode="w", engine="odf") as writer: # pandas su python 3.8 non fa aprire file xlsx e mode="a" non è supportata con engine="odf" (#@*! D:<)
        for sheetName in sheets:
            sheets[sheetName].to_excel(writer, sheetName, index=False)

    print(f"'{SUBSET_NAME}' sheet created in {INPUT_PATH}")
    
if __name__ == "__main__":
    parser = Arguments()
    parser.addAmieSettingsArguments()
    parser.addRulesFilterArguments()
    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    rulesFilter = RulesFilter(args)

    findMatchingRules(datasetFolderName, amieSettings, rulesFilter)