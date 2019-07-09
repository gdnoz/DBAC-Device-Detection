class DataSetCreator:
    """
    Can be used to create a dataset_utilities for text device_classification.
    This is done by downloading texts in a specified file and
    placing them in folders corresponding to their text device_classification category.
    """

    def __init__(self, dataset_urls_file_path: str, ):
        """
        :param dataset_urls_file_path: Filename for a .txt file which consists of category name,text names and urls.
        """
        import re

        self.dataset_urls_file_path = dataset_urls_file_path
        self._category_regex = re.compile("[A-Za-z]+:")
        self._document_regex = re.compile(".*,http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    def create_local_data_set(self, dataset_path: str):
        """
        From the given dataset_utilities url file, reach document is retrieved from the url and placed in its corresponding category folder.
        :param dataset_path: Path for where the dataset is stored.
        :return:
        """
        import IOUtilities,os

        with open(self.dataset_urls_file_path, "r") as f:
            category_path = ""

            for line in f:
                if line[:2] == "//": #Ignore Comments
                    continue

                stripped_line = line.rstrip()
                if self._category_regex.match(stripped_line):
                    category = stripped_line[:-1] #Remove last element
                    category_path = os.path.join(dataset_path,category)
                    IOUtilities.create_path(category_path)

                elif self._document_regex.match(stripped_line):
                    line_tokens = stripped_line.split(",")
                    document_name = line_tokens[0]
                    url = line_tokens[1]
                    document_path = os.path.join(category_path,document_name)

                    from web_scraping.utilities import WebScrapingUtilities

                    try:
                        text = WebScrapingUtilities.extract_text_from_url(url)
                        IOUtilities.create_file(document_path+".txt")
                        IOUtilities.write_content_to_file(text, document_path+".txt")
                    except TypeError as e:
                        print(e)
                        print("Skipping " + document_name + "...")
                    except TimeoutError as e:
                        print(e)
                        print("Skipping " + document_name + "...")
                    except Exception as e:
                        print(e)
                        print("Skipping " + document_name + "...")

if __name__ == "__main__":
    import os,constants
    import dataset_utilities.data_set_proportionality_check

    #ds_creator = DataSetCreator(os.path.join(constants.DATA_DIR,"dataset_tos_additions.txt"))
    #ds_creator.create_local_data_set(os.path.join(constants.DATA_DIR,"dataset_clean_tos"))

    ds_creator = DataSetCreator(os.path.join(constants.DATA_DIR,"dataset_urls.txt"))
    ds_creator.create_local_data_set(os.path.join(constants.DATA_DIR,"dataset_initial"))

