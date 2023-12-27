import pandas as pd
from utils.mappingRelations import replaceRelationshipIDsWithLabels
from utils.paths import getRulesRulesFilePath, getRulesExcelFilePath, getAMIEOutputFilePath
from utils.symbols import rulesExcelSymbols
from utils.arguments import AmieSettings, Arguments

def extractRulesFromAMIEOutput(datasetFolderName: str, amieSettings: AmieSettings):
    HEADER = f"{rulesExcelSymbols.RULE_COLUMN_LABEL}\t{rulesExcelSymbols.HEAD_COVERAGE_COLUMN_LABEL}\t{rulesExcelSymbols.STD_CONFIDENCE_COLUMN_LABEL}\t{rulesExcelSymbols.PCA_CONFIDENCE_COLUMN_LABEL}\t{rulesExcelSymbols.POSITIVE_EXAMPLES_COLUMN_LABEL}\t{rulesExcelSymbols.BODY_SIZE_COLUMN_LABEL}\t{rulesExcelSymbols.PCA_BODY_SIZE_COLUMN_LABEL}\t{rulesExcelSymbols.FUNCTIONAL_VARIABLE_COLUMN_LABEL}\n"
    FOOTER = "Mining done in "

    INPUT_PATH = getAMIEOutputFilePath(datasetFolderName, amieSettings)
    OUTPUT_PATH = getRulesExcelFilePath(datasetFolderName, amieSettings)

    with open(INPUT_PATH, 'r') as f:
        i = 0

        headerRowIndex = None

        for line in f:
            i += 1
            
            if headerRowIndex is None and line == HEADER:
                headerRowIndex = i
            elif line.find(FOOTER) != -1:
                break

        footerRowIndex = i - headerRowIndex - 2

    rules = pd.read_csv(INPUT_PATH, sep="\t", skiprows=headerRowIndex - 1, nrows=footerRowIndex + 1)
    rulesRulesFilePath = getRulesRulesFilePath(datasetFolderName, amieSettings)
    rules[rulesExcelSymbols.RULE_COLUMN_LABEL].to_csv(rulesRulesFilePath, sep="\t", index=False, header=False)
    print(f"New file: {rulesRulesFilePath}")
    replaceRelationshipIDsWithLabels(rules, datasetFolderName)
    
    with pd.ExcelWriter(OUTPUT_PATH, mode="w", engine="odf") as writer:
        rules.to_excel(writer, rulesExcelSymbols.ALL_SHEET_NAME, index=False)

    print(f"'{rulesExcelSymbols.ALL_SHEET_NAME}' sheet created in {OUTPUT_PATH}")

if __name__ == "__main__":
    parser = Arguments()
    parser.addAmieSettingsArguments()
    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)

    extractRulesFromAMIEOutput(datasetFolderName, amieSettings)