import csv
import pandas as pd
from utils.paths import getEntityIDFilePath, getMatrixEFilePath
import numpy as np
from utils.arguments import KaleSettings, AmieSettings, RulesFilter  

def top_scores(predictions, n):
  top_n_scores = pd.DataFrame()
  for u in list(set(predictions['users'])):
    p = predictions.loc[predictions['users'] == u ]
    top_n_scores = top_n_scores.append(p.head(n))
    #pd.concat([top_n_scores, p.head(n)])
  return top_n_scores

def read_ratings(df: pd.DataFrame, user):
  subset = df[df[0] == user]
  return list(subset[0]), list(subset[1]), list(subset[2])

def read_kale_embeddings(datasetFolderName, kaleSettings: KaleSettings, amieSettings: AmieSettings, rulesFilter: RulesFilter, dimension: int):
  matrixEFilePath = getMatrixEFilePath(datasetFolderName, amieSettings, rulesFilter, kaleSettings, dimension)
  entityIdPath = getEntityIDFilePath(datasetFolderName, kaleSettings)

  # load map dataset-matrix
  f_map = open(entityIdPath, "r", encoding="utf-8")
  #f_map = open(folder+"map.txt", "r", encoding="utf-8")
  dataset_matrix = {}

  for line in f_map:
      
      dataset_value = line.split("\t")[1].strip()
      matrix_value = line.split("\t")[0].strip()
      
      dataset_matrix[dataset_value] = matrix_value

  f_map.close()

  # open file
  f_in = open(matrixEFilePath, mode="r", encoding="utf-8")

  # read header
  header = f_in.readline().split(";")
  rows = int(header[0].split(":")[1].strip())
  columns = int(header[1].split(":")[1].strip())

  # matrix inizialization
  embeddings = np.zeros((rows, columns))
  row = 0
  col = 0

  # file reading and embeddings population
  for vector in f_in:
      emb = vector.split("\t")
      col = 0
      for value in emb:
          embeddings[row][col] = float(value)
          col += 1
      row += 1
      
  f_in.close()

  return embeddings, dataset_matrix

def matching_kale_emb_id(user, item, rating, embeddings, dataset_matrix):
  y = np.array(rating)
  dim_embeddings = len(embeddings[0])
  dim_X_cols = 2
  dim_X_rows = len(user)
  X = np.empty(shape=(dim_X_rows,dim_X_cols,dim_embeddings))

      
  #matching between ids and embeddings
  i=0
  c=0
  while i < dim_X_rows:

      # get user and item id
      user_id = user[i]
      item_id = item[i]
          
      if str(user_id) in dataset_matrix and str(item_id) in dataset_matrix:
          
          # get indices of the matrix related to user and item from the map
          ind_user = int(dataset_matrix[str(user_id)])
          ind_item = int(dataset_matrix[str(item_id)])
              
          # get embeddings of user and item
          X[c][0] = embeddings[ind_user]
          X[c][1] = embeddings[ind_item]
          
          c += 1
          
      i=i+1
      
      
  return X, y, dim_embeddings
