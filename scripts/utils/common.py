import json
from pathlib import Path
import sys
from typing import Callable, Optional

BASE_FOLDER_PATH = sys.path[0] # should be the absolute path to "/scripts" folder

UTILS_FOLDER_NAME = "utils"

def getUtilsFolderPath(*argv):
    return Path(BASE_FOLDER_PATH, UTILS_FOLDER_NAME, *argv)

def loadJsonFileFromUtilsFolder(subfolderName: str, fileName: str, description: str, hook: Optional[Callable] = None):
    path = getUtilsFolderPath(subfolderName, fileName)

    try:
        with open(path) as f:
            return json.load(f, object_hook=hook)
    except Exception as e:
        print(f"Could not load {description} from {path} ({e})\nDoes this file exist? Does it contain any errors? Please, check.")
        exit()

