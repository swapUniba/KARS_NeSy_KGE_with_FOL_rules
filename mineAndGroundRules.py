from utils.arguments import AmieSettings, Arguments
from extractRulesFromAMIEOutput import extractRulesFromAMIEOutput
from mineRules import mineRulesWithAMIE
from groundRules import groundRules

def mineAndGroundRules(datasetFolderName: str, amieSettings: AmieSettings):
    mineRulesWithAMIE(datasetFolderName, amieSettings)
    extractRulesFromAMIEOutput(datasetFolderName, amieSettings)
    groundRules(datasetFolderName, amieSettings)

if __name__ == "__main__":
    parser = Arguments()    
    parser.addAmieSettingsArguments()
    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)

    mineAndGroundRules(datasetFolderName, amieSettings)
