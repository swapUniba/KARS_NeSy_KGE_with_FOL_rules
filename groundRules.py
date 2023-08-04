from utils.arguments import AmieSettings, Arguments
from utils.paths import getUserItemPropRelationIDFilePath, getUserItemPropTrainFilePath, getRulesRulesFilePath, getRulesSubsetAllFolderPath, getAllGroundingsFilePath, GROUND_ALL_RULES_FILE_PATH
import os
import subprocess

def groundRules(datasetFolderName: str, amieSettings: AmieSettings):
    rulesSubsetAllFolderPath = getRulesSubsetAllFolderPath(datasetFolderName, amieSettings)

    if not os.path.exists(rulesSubsetAllFolderPath):
        os.makedirs(rulesSubsetAllFolderPath)
        print(f"New path: {rulesSubsetAllFolderPath}")

    print("Rules grounding process might take up to several hours. Please, wait.")
    
    relationID = getUserItemPropRelationIDFilePath(datasetFolderName)
    train = getUserItemPropTrainFilePath(datasetFolderName)
    rules = getRulesRulesFilePath(datasetFolderName, amieSettings)
    groundings = getAllGroundingsFilePath(datasetFolderName, amieSettings)

    subprocess.check_call(["java", "-jar", GROUND_ALL_RULES_FILE_PATH, relationID, train, rules, groundings])
    
    print(f"New file: {groundings}")
    print("Rules grounding process completed.")

if __name__ == "__main__":
    parser = Arguments()
    parser.addAmieSettingsArguments()
    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)

    groundRules(datasetFolderName, amieSettings)