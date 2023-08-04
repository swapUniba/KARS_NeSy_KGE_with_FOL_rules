import csv
import tensorflow as tf
from tensorflow import keras
from predict import generatePredictions
from utils.amarMisc import matching_kale_emb_id, read_kale_embeddings, read_ratings
from utils.arguments import AmieSettings, Arguments, KaleSettings, RulesFilter, AmarSettings
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension
from utils.exceptions import AmarException
from utils.paths import getUserItemAmarTrainFilePath, getResultsFolderPath, getModelFilePath
import os
import tensorflow as tf
import pandas as pd

def read_kale_ratings(filename, folder):
    
  # load map dataset-matrix
  f_map = open(folder+"_map-dataset-matrix.txt", "r", encoding="utf-8")
  dataset_matrix = {}

  for line in f_map:
      
      dataset_value = line.split("\t")[0].strip()
      matrix_value = line.split("\t")[1].strip()
      
      dataset_matrix[dataset_value] = matrix_value

  f_map.close()


  user=[]
  item=[]
  rating=[]

  #reading item ids
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    #next(csv_reader)
    for row in csv_reader:
        if row[0] in dataset_matrix and row[1] in dataset_matrix:
            user.append(int(row[0]))
            item.append(int(row[1]))
            rating.append(int(row[2]))
  return user, item, rating

def isolate_kale_user_item_emb(users, items, graph_embeddings, dataset_matrix):

  embs = []
  i=0
  user_map = {}
  item_map = {}

  for usr in users:
    ind_u = int(dataset_matrix[str(usr)])
    embs.append(graph_embeddings[ind_u])
    user_map[usr] = i
    i+=1

  for itm in items:
    ind_i = int(dataset_matrix[str(itm)])
    embs.append(graph_embeddings[ind_i])
    item_map[itm] = i
    i+=1


  return embs, user_map, item_map


import tensorflow as tf
from tensorflow import keras

#from models.DataGenerator import DataGenerator as dg

# define the keras model
def run_model(X, y, dim_embeddings, epochs, batch_size):
  model = keras.Sequential()

  input_users = keras.layers.Input(shape=(dim_embeddings,))

  x1 = keras.layers.Dense(512, activation=tf.nn.relu)(input_users)
  x1_2 = keras.layers.Dense(256, activation=tf.nn.relu)(x1)
  x1_3 = keras.layers.Dense(128, activation=tf.nn.relu)(x1_2)

  input_items = keras.layers.Input(shape=(dim_embeddings,))

  x2 = keras.layers.Dense(512, activation=tf.nn.relu)(input_items)
  x2_2 = keras.layers.Dense(256, activation=tf.nn.relu)(x2)
  x2_3 = keras.layers.Dense(128, activation=tf.nn.relu)(x2_2)

  concatenated = keras.layers.Concatenate()([x1_3, x2_3])

  d1 = keras.layers.Dense(64, activation=tf.nn.relu)(concatenated)
  d2 = keras.layers.Dense(64, activation=tf.nn.relu)(d1)
  out = keras.layers.Dense(1, activation=tf.nn.sigmoid)(d2)

  model = keras.models.Model(inputs=[input_users,input_items],outputs=out)
  model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9), metrics=['accuracy'])
  model.fit([X[:,0],X[:,1]], y, epochs=epochs, batch_size=batch_size)

  return model

def runAmar(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, amieSettings: AmieSettings):
  try:
    # set input files and output files
    dest = getResultsFolderPath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
    
    modelFilePath = getModelFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)

    # create folders if needed
    if not os.path.exists(dest):
        os.makedirs(dest)
        print(f"New path: {dest}")
    
    # load kale embeddings for training and the map dataset -> matrix
    ent_embeddings, dataset_matrix = read_kale_embeddings(datasetFolderName, kaleSettings, amieSettings, rulesFilter, dimension)
    
    # read user-item/user-item-prop train set

    # user-item-prop train
    #user, item, rating = read_ratings('datasets/movielens/train2id.tsv')
    
    # user-item train
    trainPath = getUserItemAmarTrainFilePath(datasetFolderName)
    trainTriples = pd.read_csv(trainPath, sep='\t', header=None)
    user, item, rating = list(trainTriples[0]), list(trainTriples[1]), list(trainTriples[2])
    
    # match KALE ids with dataset ids
    X, y, dim_embeddings = matching_kale_emb_id(user, item, rating, ent_embeddings, dataset_matrix)
    
    print("\tEmbedding dimension: ", dim_embeddings)
    
    # run model
    batch = 512
    epo = 25
    model = run_model(X, y, dim_embeddings, epochs=epo, batch_size=batch)
        
    # creates a HDF5 file 'model.h5'
    model.save(modelFilePath)
    print(f"New file: {modelFilePath}")

    generatePredictions(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings, ent_embeddings, dataset_matrix, model)
  except Exception as e:
    raise AmarException("failed to train the model", e)

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

  forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: runAmar(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dim, amieSettings))