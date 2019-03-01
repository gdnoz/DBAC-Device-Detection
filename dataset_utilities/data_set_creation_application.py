if __name__ == "__main__":
    from dataset_utilities.data_set_creation import DataSetCreator
    import os,constants

    ds_creator = DataSetCreator(constants.DATA_SET_URLS_FILE_PATH)
    ds_creator.create_local_data_set(constants.DATA_SET_PATH)


