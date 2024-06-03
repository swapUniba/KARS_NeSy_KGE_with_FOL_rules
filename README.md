# Knowledge-Aware Recommender Systems based on Neuro Symbolic Knowledge Graph Embeddings with First-Order Logic Rules
Source code and data for the paper "Knowledge-Aware Recommender Systems based on Neuro Symbolic Knowledge Graph Embeddings with First-Order Logic Rules".

This repo contains source code and data of the mentioned paper, which aims at injecting First-Order Logic rules during the process of Knowledge Graph Embedding in order to better represent users and items in the context of Knowledge-Aware Recommender Systems.

## Results reproducibility

In order to replicate our results, please find the generated prediction lists in the `predictions` folder.
You can evaluate them by using the [Elliot](https://elliot.readthedocs.io/en/latest/) framework. To do so, first install Elliot and its depencendes (please follow the original [documentation](https://elliot.readthedocs.io/en/latest/) for more details); then, move the content of the `data` folder of this repository into the `data` folder of Elliot; in this way, each dataset will be loadable by Elliot. Then, move `elliot_evaluation.yml` and file from this repo to the `config_file/` folder of Elliot. Finally, create a folder named `predictions/kge_fol_rules/<dataset>/` in the Elliot folder, and move the `.tsv` files in the `predictions` folder into this new folder (in the correct <dataset> folder, of course).
Then, you can evaluate them by running the command
```sh
python3 start_experiments.py -config=elliot_evaluation
```
The results of the evaluation will be stored in the `external_results/<dataset>/recs/` folder, including paired ttest or Wilcoxon test (that are set to `True` in our `elliot_evaluation.yml` file).

Alternatively, you can run the whole pipeline from scratch.

## Pre-requirements
In order to reproduce the entire pipeline, it is necessary to install (1) Java 1.7 and (2) Python 3.7 or more, with Keras installed. The experiments have been performed on a machine with Ubuntu 20.04.4 LTS. 
It is reasonable that more recent versions of both Java and Python are still compatible with the source code. For further details about Python packages required to reproduce our source code, please check the [requirements](https://github.com/swapUniba/KARS_NeSy_KGE_with_FOL_rules/blob/main/scripts/req.txt) file.

## Pipeline
The overall pipeline can be split into three main steps:
1. Mine FOL rules from the dataset
2. Learn KGE by injecting FOL rules during the process
3. Train and test the recommendation model with the embeddings

In the following, we will describe how each of these steps can be performed by using our source code, and where the input and output data are stored.
First, we will describe the structure of each dataset.

### Dataset structure
Dataset can be found in two versions: `user-item` and `user-item-prop`. The main difference is that in the former we only encode user-item interactions (likes and dislikes), while in the latter we also encode KG triples related to the items in the dataset. We also provided the two mappings: `mapping_items.tsv` and `mapping_relations.tsv` that just map the IDs of items and relations to corresponding strings.
Within each folder (`user-item` or `user-item-prop`) we included the files necessary to mine the FOL rules, learn the KGE and train the recommendation models: `entityid.txt` and `relationid.txt` map our entities and relations with contiguos ids, that are necessary to learn the KGE; the files `train.txt`, `valid.txt` and `test.txt` and remapped versions of the files `kale_train.txt`, `kale_valid.txt` and `kale_test.txt`, since the models we explit (AMIE and KALE) need their own continguous mappings; finally, `amar_train.tsv` and `amar_test.tsv` are the files used to train and test the recommender system.


### 1. FOL mining
The first step is the mining of the rules form a dataset - let us take `dbbook` as an example. 
Given the `dbbook` dataset split as described in the previous section, and supposing we want to mine rules of lenght 3 (that is, 2 atoms in the body and 1 atom in the head), we need to run the command:
```sh
python3 mineAndGroundRules.py --maxad=3 dbbook
```
At the end of the process, you will find the folder `with_rules\maxad_3\` in the dataset folder, which will contain all the mined rules and the related groudings (instances of the rules, `with_rules\maxad_3\all\groundings.txt`) in several format, including a easy-to-read `.odf` file that will also contain, for each rule, the value of each metrics (e.g., PCA confidence or number of positive examples).

To investigate further parameters of the rule mining process, you can run
```sh
python3 mineAndGroundRules.py -h
```
and check all the other possible parameters.
In the following table we list some of these parameters:
|Parameter | Description|
| ------ | ------ |
|MAX_AD_FLAG | maximum number of atoms per rule|
|MIN_STD_CONFIDENCE_FLAG |minimum standard confidence per rule|
|MIN_POSITIVE_EXAMPLES_FLAG |minimum amount of positive examples per rule|
|MIN_PCA_CONFIDENCE_FLAG |minimum PCA confidence per rule|
|LIKE_ONLY_FLAG |weather to consider only those rules which head includes a like relationship|


### 2. KGE learning
Now we want to learn the KGE for `dbbook` by using the rules mined during the previous step, and we want the embeddings of dimension `10` (all the other parameters, such as the number of epochs of the learning step, are left as default values). All we need to do is running the following command:
```sh
python3 runKale.py --maxad=3 --dims=10 --itemProperties dbbook
```
At the end of the process, we will find the embeddings in the folder `with_rules\maxad_3\all\embeddings\with_props\d0.1-ge0.05-gr0.05-w0.01-mb100-i500-s50\dim10\MatrixE.best`. In this file, each row of the matrix corresponds to the embedding of an entity, and the mapping is `entityid.txt` described during the dataset structure description.

To investigate further parameters of the KGE learning process and set other parameters, you can run
```sh
python3 runKale.py -h
```
and check all the other possible parameters.

### 3. Train the recommendation model and evaluate

Finally, in order to train the recommendation model by using the KGE learned during the previous step, all we need to do is running the following command:

```sh
python3 runAmar.py --maxad=3 --dims=10 --itemProperties dbbook
```
This script will train the recommendation model by using the selected KGE and will produce two recommendation lists (`top5` and `top10`) that will be stored in the folder `with_rules\maxad_3\...\dim10\predictions\` as `.tsv` files; moreover, the folder `with_rules\maxad_3\...\dim10\predictions\` will contain the `.h5` trained model.

More parameters for the training can be set, and they can be visualized by running the command
```sh
python3 runAmar.py -h
```

Finally, the evaluation of the just generated prediction list can be performed with any evaluation tool; in our experiments, we used [Elliot](https://elliot.readthedocs.io/en/latest/): with Elliot it is possible to provide one (or more) recommendation list (as a ProxyRecommender model, or RecommendationFolder model) that are evaluated by using the `test.tsv` file provided. An example of the configuration file we used is provided in this repository, named `elliot_evaluation.yml`.

In order to evaluate the recommendation list, you need to install Elliot and its depencendes; then, move the content of the `data` folder of this repository into the `data` folder of Elliot; in this way, each dataset will be loadable by Elliot. Then, move `elliot_evaluation.yml` and file from this repo to the `config_file/` folder of Elliot. Finally, create a folder named `predictions/kge_fol_rules/<dataset>/` in the Elliot folder, and move the `.tsv` file generated at the previous step into this new folder (in the correct <dataset> folder, of course).
In this way, Elliot will be able to evaluate the generated recommendation list by following the instruction reported in the configuration file, using the ground truth that can be found in the `data` folder.

It is possible to start the evaluation of the prediction list by running the command:
```sh
python3 start_experiments.py -config=elliot_evaluation
```
The results of the evaluation will be stored in the `external_results/<dataset>/recs/` folder, including paired ttest or Wilcoxon test (that are set to `True` in our `elliot_evaluation.yml` file).

## Credits
Thanks to the student Gianmarco Turchiano for his technical support.