class BacnetClassificationResult:
    predicted_class = ""
    score = 0.0

    def __init__(self, predicted_class: str, score: float):
        self.predicted_class = predicted_class
        self.score = score

    def __str__(self):
        return "("+self.predicted_class+","+str(self.score)+")"

class BacnetClassification:
    '''
    Performs device_classification on bacnet test_devices based on text retrieved from object queries, which is provided as input.
    '''

    def __init__(self, classification_threshold: float, scraping_threshold: float):
        from device_classification.text_classification import DeviceClassifier
        from web_scraping.scraping import RelevantTextScraper
        self.threshold = classification_threshold
        self.text_scraper = RelevantTextScraper(scraping_threshold)
        self.classifier = DeviceClassifier(threshold=classification_threshold)

    def classify_bacnet_objects(self, queried_objects: str) -> BacnetClassificationResult:
        '''
        Takes the queried objects of a device as input, cleans the input and preforms device_classification.
        :param queried_objects: The queried objects of the device in json format
        :return: BacnetClassificationResult containing predicted class and score.
        '''
        from web_scraping.google import GoogleCustomSearchAPI
        from bacnet.utilities import BacnetUtilities
        from web_scraping.bing import BingSearchAPI
        import operator

        '''
        Preparing classification based on search engines.
        '''
        search_terms = ""

        deviceType = BacnetUtilities.get_deviceType_from_query(queried_objects)
        description = BacnetUtilities.get_description_from_query(queried_objects)

        if deviceType != "":
            search_terms = deviceType
        elif description != "":
            search_terms = description
        else:
            vendor_name = BacnetUtilities.get_vendor_name_from_query(queried_objects)
            model_name = BacnetUtilities.get_model_name_from_query(queried_objects)

            search_terms = vendor_name + " " + model_name

        '''
        Classification based on Bing and Google
        '''
        print("Classifying using Bing and Google...")

        snippets = GoogleCustomSearchAPI.search_text(search_terms) + BingSearchAPI.first_ten_snippets(search_terms)

        classification_result = self.classifier.predict_snippets(snippets)

        return BacnetClassificationResult(classification_result.predicted_class,classification_result.prediction_probability)


