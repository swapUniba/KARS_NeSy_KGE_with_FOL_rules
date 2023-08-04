import argparse
import os
import subprocess
from utils.arguments import AmieSettings, Arguments
from utils.paths import AMIE_INIT_FILE_PATH, getAMIEOutputFilePath, getUserItemPropKaleTrainFilePath, getMaxAdFolderPath

def mineRulesWithAMIE(datasetFolderName: str, amieSettings: AmieSettings):    
    maxAdFolderPath = getMaxAdFolderPath(datasetFolderName, amieSettings)
    
    if not os.path.exists(maxAdFolderPath):
        os.makedirs(maxAdFolderPath)
        print(f"New path: {maxAdFolderPath}")

    INPUT_PATH = getUserItemPropKaleTrainFilePath(datasetFolderName)
    OUTPUT_PATH = getAMIEOutputFilePath(datasetFolderName, amieSettings)

    print("Rule mining process might take up to several hours. Please, wait.")

    with open(OUTPUT_PATH, 'w') as f:
        subprocess.check_call(["java", "-jar", AMIE_INIT_FILE_PATH, INPUT_PATH, "-maxad", str(amieSettings.maxad)], stdout=f)

    print(f"New file: {OUTPUT_PATH}")

    print("Rule mining process completed.")

if __name__ == "__main__":
    parser = Arguments()
    parser.addAmieSettingsArguments()
    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)

    mineRulesWithAMIE(datasetFolderName, amieSettings)