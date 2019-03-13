import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PMML_DIR = os.path.join(ROOT_DIR,"classification/pmml/")
MUDFILES_DIR = os.path.join(ROOT_DIR,"data/mudfiles")
DATA_DIR = os.path.join(ROOT_DIR,"data")
MUD_FILE_URLS_FILE_PATH = os.path.join(DATA_DIR,"mud_file_urls.csv")
DATA_SET_URLS_FILE_PATH = os.path.join(DATA_DIR,"dataset_urls.txt")
DATA_SET_PATH = os.path.join(DATA_DIR,"dataset")
