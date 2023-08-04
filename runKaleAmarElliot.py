from runKale import runKale
from utils.arguments import Arguments, AmieSettings, KaleSettings, RulesFilter, AmarSettings
from runAmarElliot import runAmarElliot
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension

def runKaleAmarElliot(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, amieSettings: AmieSettings):    
    runKale(datasetFolderName, rulesFilter, kaleSettings, dimension, amieSettings)
    runAmarElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings)

if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()
    parser.addAmarSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    kaleSettings = KaleSettings(args)
    rulesFilter = RulesFilter(args)
    amarSettings = AmarSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: runKaleAmarElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dim, amieSettings))