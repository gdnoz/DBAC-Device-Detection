import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PMML_DIR = os.path.join(ROOT_DIR,"device_classification/pmml/")
MUDFILES_DIR = os.path.join(ROOT_DIR,"data/mudfiles")
DATA_DIR = os.path.join(ROOT_DIR,"data")
MUD_FILE_URLS_FILE_PATH = os.path.join(DATA_DIR,"mud_file_urls.csv")
DATA_SET_URLS_FILE_PATH = os.path.join(DATA_DIR,"dataset_urls_expanded_20.txt")
DATA_SET_PATH = os.path.join(DATA_DIR,"dataset")
DATA_SET_PATH_TOS = os.path.join(DATA_DIR,"dataset_clean_tos")
TEMP_FOLDER = os.path.join(ROOT_DIR,"temp")
BACNET_TEST_DEVICES_FOLDER = os.path.join(ROOT_DIR, "bacnet/local_device_applications/test_devices")