from utils.paths import getUserItemAmarAllItemsFilePath, getModelFilePath, getUserItemAmarTestFilePath, getTopPredictionsFolderPath, getPredictions1FilePath
import pandas as pd
import numpy as np
import os
from tensorflow import keras
from utils.exceptions import AmarException
from utils.amarMisc import read_ratings, matching_kale_emb_id, top_scores, read_kale_embeddings, top_scores
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension
from utils.arguments import Arguments, RulesFilter, KaleSettings, AmarSettings, AmieSettings

def generatePredictions(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, amieSettings: AmieSettings, ent_embeddings: np.ndarray, dataset_matrix: dict, model: keras.Sequential):    
    try:
        if amarSettings.allItems:
            amarTriples = getUserItemAmarAllItemsFilePath(datasetFolderName)
        else:
            amarTriples = getUserItemAmarTestFilePath(datasetFolderName)

        testTriples = pd.read_csv(amarTriples, sep='\t', header=None)

        usersSet = set(testTriples[0])

        for u in usersSet:
            # user-item test
            user, item, rating = read_ratings(testTriples, u)

            # select kale embeddings for predictions
            X, y, dim_embeddings = matching_kale_emb_id(user, item, rating, ent_embeddings, dataset_matrix)

            # predict   
            print("\tPredicting...")
            score = model.predict([X[:,0],X[:,1]])

            # write predictions
            print("\tComputing predictions...")
            score = score.reshape(1, -1)[0,:]
            predictions = pd.DataFrame()
            predictions['users'] = np.array(user)
            predictions['items'] = np.array(item)
            predictions['scores'] = score

            predictions = predictions.sort_values(by=['users', 'scores'], ascending=[True, False])

            for k in amarSettings.topK:
                topFolderPath = getTopPredictionsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, k)

                if os.path.exists(topFolderPath):
                    mode = 'a'
                else:
                    os.makedirs(topFolderPath)
                    print(f"New path: {topFolderPath}")
                    mode = 'w'

                topPredictionsFilePath = getPredictions1FilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, amarSettings, dimension, k)

                topScores = top_scores(predictions, k)
                topScores.to_csv(topPredictionsFilePath, mode=mode, sep='\t',header=False,index=False)
                print(f"Updated with user {u}: {topPredictionsFilePath}")
    except Exception as e:
        raise AmarException("failed to produce predictions", e)

def predict(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, amieSettings: AmieSettings):
    modelPath = getModelFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
    model = keras.models.load_model(modelPath)
    ent_embeddings, dataset_matrix = read_kale_embeddings(datasetFolderName, kaleSettings, amieSettings, rulesFilter, dimension)
    generatePredictions(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings, ent_embeddings, dataset_matrix, model)

if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()
    parser.addAmarSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    rulesFilter = RulesFilter(args)
    kaleSettings = KaleSettings(args)
    amarSettings = AmarSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: predict(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dim, amieSettings))