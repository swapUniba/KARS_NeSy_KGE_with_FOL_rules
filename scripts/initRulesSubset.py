from utils.arguments import AmieSettings, Arguments, RulesFilter
from findMatchingRules import findMatchingRules
from findGroundings import findGroundings

def initRulesSubset(datasetFolderName: str, amieSettings: AmieSettings, rulesFilter: RulesFilter):
    findMatchingRules(datasetFolderName, amieSettings, rulesFilter)
    findGroundings(datasetFolderName, amieSettings, rulesFilter)

if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsArguments()
    parser.addRulesFilterArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    rulesFilter = RulesFilter(args)
    
    initRulesSubset(datasetFolderName,amieSettings, rulesFilter)