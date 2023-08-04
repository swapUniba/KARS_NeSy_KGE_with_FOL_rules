import os
from pathlib import Path
import subprocess
from utils.arguments import Arguments
from utils.paths import getUserItemAmarAllItemsFilePath, getMappingUsersFilePath, getMappingItemsFilePath, getUserItemAmarTestFilePath, getUserItemAmarTestLikeOnlyFilePath, getUserItemAmarTrainFilePath, getUserItemKaleTestFilePath, getUserItemKaleTrainFilePath, getUserItemKaleValidFilePath, getUserItemEntityIDFilePath, getUserItemRelationIDFilePath, getUserItemTrainFilePath, getUserItemTestFilePath, getUserItemValidFilePath, getUserItemFolderPath, getUserItemPropAmarTestFilePath, getUserItemPropAmarTrainFilePath, CONVERT_DATA_FORM_FILE_PATH, getUserItemPropKaleTrainFilePath, getUserItemPropKaleValidFilePath, getUserItemPropKaleTestFilePath, getUserItemPropTrainFilePath, getUserItemPropValidFilePath, getUserItemPropTestFilePath, getUserItemPropEntityIDFilePath, getUserItemPropRelationIDFilePath
from utils.symbols import rulesExcelSymbols, USER_ITEM_RELATIONSHIPS_LABELS
import pandas as pd
from utils.mappingRelations import getMappingRelationsLabelsToIDs

def _filterTriples(inputFilePath: Path, validRelationshipsIDs: list, relationshipColumnIndex: int, outputFilePath: Path):
    try:
        df = pd.read_csv(inputFilePath, sep="\t", header=None)
        newDf = df[df[relationshipColumnIndex].map(lambda relationshipID: relationshipID in validRelationshipsIDs)]
        newDf.to_csv(outputFilePath, sep="\t", header=None, index=None)
    except pd.errors.EmptyDataError:
        f = open(outputFilePath, 'w')
        f.close()

    print(f"New file: {outputFilePath}")

def initDataset(datasetFolderName: str):
    uipKaleTrainPath = getUserItemPropKaleTrainFilePath(datasetFolderName)
    uipKaleValidPath = getUserItemPropKaleValidFilePath(datasetFolderName)
    uipKaleTestPath = getUserItemPropKaleTestFilePath(datasetFolderName)
    
    if not os.path.exists(uipKaleTestPath):
        f = open(uipKaleTestPath, "w")
        f.close()

    uipTrainPath = getUserItemPropTrainFilePath(datasetFolderName)
    uipValidPath = getUserItemPropValidFilePath(datasetFolderName)
    uipTestPath = getUserItemPropTestFilePath(datasetFolderName)
    uipEntityIDPath = getUserItemPropEntityIDFilePath(datasetFolderName)
    uipRelationIDPath = getUserItemPropRelationIDFilePath(datasetFolderName)

    subprocess.check_call(["java", "-jar", CONVERT_DATA_FORM_FILE_PATH, uipKaleTrainPath, uipKaleValidPath, uipKaleTestPath, uipTrainPath, uipValidPath, uipTestPath, uipEntityIDPath, uipRelationIDPath])

    print(f"New file: {uipTrainPath}")
    print(f"New file: {uipValidPath}")
    print(f"New file: {uipTestPath}")
    print(f"New file: {uipEntityIDPath}")
    print(f"New file: {uipRelationIDPath}")
    
    userItemFolderPath = getUserItemFolderPath(datasetFolderName)

    if not os.path.exists(userItemFolderPath):
        os.makedirs(userItemFolderPath)
        print(f"New path: {userItemFolderPath}")

    uipAmarTrainPath = getUserItemPropAmarTrainFilePath(datasetFolderName)
    uipAmarTestPath = getUserItemPropAmarTestFilePath(datasetFolderName)

    uiKaleTrainPath = getUserItemKaleTrainFilePath(datasetFolderName)
    uiKaleTestPath = getUserItemKaleTestFilePath(datasetFolderName)
    uiKaleValidPath = getUserItemKaleValidFilePath(datasetFolderName)
    
    uiAmarTestPath = getUserItemAmarTestFilePath(datasetFolderName)
    uiAmarTestPathLikeOnly = getUserItemAmarTestLikeOnlyFilePath(datasetFolderName)

    uiAmarTrainPath = getUserItemAmarTrainFilePath(datasetFolderName)

    relationshipsIDs = getMappingRelationsLabelsToIDs(datasetFolderName)
    
    likeRelationshipID = relationshipsIDs[rulesExcelSymbols.LIKE_RELATIONSHIP_LABEL]
    dislikeRelationshipID = relationshipsIDs[rulesExcelSymbols.DISLIKE_RELATIONSHIP_LABEL]

    userItemRelationshipIDs = [likeRelationshipID, dislikeRelationshipID]

    for label in USER_ITEM_RELATIONSHIPS_LABELS:
        if label in relationshipsIDs:
            userItemRelationshipIDs.append(relationshipsIDs[label])

    KALE_RELATIONSHIP_COLUMN = 1

    AMAR_USER_COLUMN = 0
    AMAR_ITEM_COLUMN = 1
    AMAR_RELATIONSHIP_COLUMN = 2

    _filterTriples(uipKaleTrainPath, userItemRelationshipIDs, KALE_RELATIONSHIP_COLUMN, uiKaleTrainPath)
    _filterTriples(uipKaleValidPath, userItemRelationshipIDs, KALE_RELATIONSHIP_COLUMN, uiKaleValidPath)
    _filterTriples(uipKaleTestPath, userItemRelationshipIDs, KALE_RELATIONSHIP_COLUMN, uiKaleTestPath)
    
    _filterTriples(uipAmarTrainPath, userItemRelationshipIDs, AMAR_RELATIONSHIP_COLUMN, uiAmarTrainPath)

    _filterTriples(uipAmarTestPath, userItemRelationshipIDs, AMAR_RELATIONSHIP_COLUMN, uiAmarTestPath)
    _filterTriples(uipAmarTestPath, [likeRelationshipID], AMAR_RELATIONSHIP_COLUMN, uiAmarTestPathLikeOnly)

    uiTrainPath = getUserItemTrainFilePath(datasetFolderName)
    uiValidPath = getUserItemValidFilePath(datasetFolderName)
    uiTestPath = getUserItemTestFilePath(datasetFolderName)
    uiEntityIDPath = getUserItemEntityIDFilePath(datasetFolderName)
    uiRelationIDPath = getUserItemRelationIDFilePath(datasetFolderName)

    subprocess.check_call(["java", "-jar", CONVERT_DATA_FORM_FILE_PATH, uiKaleTrainPath, uiKaleValidPath, uiKaleTestPath, uiTrainPath, uiValidPath, uiTestPath, uiEntityIDPath, uiRelationIDPath])

    print(f"New file: {uiTrainPath}")
    print(f"New file: {uiValidPath}")
    print(f"New file: {uiTestPath}")
    print(f"New file: {uiEntityIDPath}")
    print(f"New file: {uiRelationIDPath}")

    allItemsPath = getUserItemAmarAllItemsFilePath(datasetFolderName)

    test = pd.read_csv(uiAmarTestPath, sep="\t", header=None)
    train = pd.read_csv(uiAmarTrainPath, sep="\t", header=None)

    test.to_csv(allItemsPath, sep="\t", mode="w", header=None, index=None)

    usersSet = set(test[AMAR_USER_COLUMN].append(train[AMAR_USER_COLUMN]))
    itemsSet = set(test[AMAR_ITEM_COLUMN].append(train[AMAR_ITEM_COLUMN]))

    print(f"Users: {len(usersSet)}; Items: {len(itemsSet)}")

    maxCount = 0

    for user in usersSet:
        userTrainItemsSet = set(train[train[AMAR_USER_COLUMN] == user][AMAR_ITEM_COLUMN])
        userTestItemsSet = set(test[test[AMAR_USER_COLUMN] == user][AMAR_ITEM_COLUMN])
        userItemsSet = itemsSet - userTrainItemsSet - userTestItemsSet

        count = len(userItemsSet) + len(userTestItemsSet)

        print(f"User {user}: {count} items")

        maxCount = count if count > maxCount else maxCount

        missingItems = pd.DataFrame(columns=[AMAR_USER_COLUMN, AMAR_ITEM_COLUMN, AMAR_RELATIONSHIP_COLUMN])

        for item in userItemsSet:
            record = [None] * 3
            record[AMAR_USER_COLUMN] = user
            record[AMAR_ITEM_COLUMN] = item
            record[AMAR_RELATIONSHIP_COLUMN] = dislikeRelationshipID    
            missingItems.loc[len(missingItems)] = record
        
        missingItems.to_csv(allItemsPath, sep="\t", mode="a", header=None, index=None)

    print(f"Max items: {maxCount}")

    print(f"New file: {allItemsPath}")

if __name__ == "__main__":
    parser = Arguments()
    (datasetFolderName, args) = parser.parse()

    initDataset(datasetFolderName)