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

    def __init__(self, classification_threshold: float):
        from device_classification.text_classification import DeviceClassifier
        self.threshold = classification_threshold
        self.classifier = DeviceClassifier(threshold=classification_threshold)

    def classify_bacnet_objects(self, queried_objects: str) -> BacnetClassificationResult:
        '''
        Takes the queried objects of a device as input, cleans the input and preforms device_classification.
        :param queried_objects: The queried objects of the device in json format
        :return: BacnetClassificationResult containing predicted class and score.
        '''

        classification_result = self.classifier.predict_text(queried_objects)

        if classification_result.prediction_probability > self.threshold and classification_result.predicted_class is not "":
            return BacnetClassificationResult(classification_result.predicted_class,classification_result.prediction_probability)

        return BacnetClassificationResult("",0.0)

if __name__ == "__main__":
    from bacnet.local_device_applications.cdrbac import cdrbac
    from mud.scraping import RelevantTextScraper
    from web_scraping.bing import BingSearchAPI

    bc = BacnetClassification(0.0)

    text = cdrbac.run_application()

    print(bc.classify_bacnet_objects(text))

    urls = BingSearchAPI.first_ten_results(text)

    text_from_urls = RelevantTextScraper(set(urls), 0.1).extract_text_from_urls()

    print(bc.classify_bacnet_objects(text_from_urls))