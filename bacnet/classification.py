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
    Performs device_classification on bacnet devices based on text retrieved from object queries, which is provided as input.
    '''

    def __init__(self, classification_threshold: float, scraping_threshold: float):
        from device_classification.text_classification import DeviceClassifier
        self.threshold = classification_threshold
        self.scraping_threshold = scraping_threshold
        self.classifier = DeviceClassifier(threshold=classification_threshold)

    def classify_bacnet_objects(self, queried_objects: str) -> BacnetClassificationResult:
        '''
        Takes the queried objects of a device as input, cleans the input and preforms device_classification.
        :param queried_objects: The queried objects of the device in json format
        :return: BacnetClassificationResult containing predicted class and score.
        '''
        from web_scraping.scraping import RelevantTextScraper
        from web_scraping.bing import BingSearchAPI
        from web_scraping.google import GoogleCustomSearchAPI
        from bacnet.utilities import BacnetUtilities

        '''
        Classification based bacnet objects query
        '''

        print("Classifying based on objects query...")

        classification_result = self.classifier.predict_text(queried_objects)

        if classification_result.prediction_probability > self.threshold and classification_result.predicted_class is not "":
           return BacnetClassificationResult(classification_result.predicted_class,classification_result.prediction_probability)

        print("Failed...")

        '''
        Preparing classification based on search engines.
        '''
        search_terms = ""

        description = BacnetUtilities.get_description_from_query(queried_objects)

        if description != "":
            search_terms = description
        else:
            vendor_name = BacnetUtilities.get_vendor_name_from_query(queried_objects)
            model_name = BacnetUtilities.get_model_name_from_query(queried_objects)
            device_object_name = BacnetUtilities.get_device_object_name_from_query(queried_objects) #Not useful?

            search_terms = vendor_name + " " + model_name# + " " + device_object_name

        print("Search terms: " + search_terms)


        '''
        Classification based on Bing
        '''

        print("Classifying using Bing...")

        urls = BingSearchAPI.first_ten_results(search_terms)

        text_from_urls = RelevantTextScraper(set(urls), self.scraping_threshold).extract_text_from_urls()

        classification_result = self.classifier.predict_text(text_from_urls)

        if classification_result.prediction_probability > self.threshold and classification_result.predicted_class is not "":
            return BacnetClassificationResult(classification_result.predicted_class,classification_result.prediction_probability)

        print("Failed...")

        '''
        Classification based on Google
        '''

        print("Classifying using Google...")

        urls = GoogleCustomSearchAPI.search(search_terms)

        text_from_urls = RelevantTextScraper(set(urls), self.scraping_threshold).extract_text_from_urls()

        classification_result = self.classifier.predict_text(text_from_urls)

        if classification_result.prediction_probability > self.threshold and classification_result.predicted_class is not "":
            return BacnetClassificationResult(classification_result.predicted_class,classification_result.prediction_probability)
        else:
            print("Failed...")
            return BacnetClassificationResult("No_classification",0.0)


if __name__ == "__main__":
    from bacnet.local_device_applications.cdrbac import cdrbac
    from web_scraping.scraping import RelevantTextScraper
    from bacnet.utilities import BacnetUtilities

    text = cdrbac.run_application()

    bc = BacnetClassification(0.2,0.1)

    print(bc.classify_bacnet_objects(text))


