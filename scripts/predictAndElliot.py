from utils.arguments import Arguments, RulesFilter, KaleSettings, AmarSettings, AmieSettings, ElliotSettings
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension
from predict import predict
from runElliot import runElliot

def predictAndElliot(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, elliotSettings: ElliotSettings, dimension: int, amieSettings: AmieSettings):
    predict(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings)
    runElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, elliotSettings, dimension, amieSettings)

if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()
    parser.addAmarSettingsArguments()
    parser.addElliotSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    rulesFilter = RulesFilter(args)
    kaleSettings = KaleSettings(args)
    amarSettings = AmarSettings(args)
    elliotSettings = ElliotSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: predictAndElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, elliotSettings, dim, amieSettings))