from runAmar import runAmar
from utils.arguments import Arguments, AmieSettings, KaleSettings, RulesFilter, AmarSettings, ElliotSettings
from runElliot import runElliot
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension

def runAmarElliot(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, elliotSettings: ElliotSettings, dimension: int, amieSettings: AmieSettings):    
    runAmar(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings)
    runElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings)

if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()
    parser.addAmarSettingsArguments()
    parser.addElliotSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    kaleSettings = KaleSettings(args)
    rulesFilter = RulesFilter(args)
    amarSettings = AmarSettings(args)
    elliotSettings = ElliotSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: runAmarElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, elliotSettings, dim, amieSettings))