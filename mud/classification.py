class MudClassificationResult:
    predicted_class = ""
    score = 0.0

    def __init__(self, predicted_class: str, score: float):
        self.predicted_class = predicted_class
        self.score = score

class MudClassification:
    """
    Given a mud file as input, the file will be used to classify the type of the device.
    """

    def __init__(self, classification_threshold: float, scraping_threshold: float):
        from device_classification.text_classification import DeviceClassifier
        from web_scraping.scraping import RelevantTextScraper
        self.threshold = classification_threshold
        self.scraping_threshold = scraping_threshold
        self.classifier = DeviceClassifier(threshold=classification_threshold)
        self.text_scraper = RelevantTextScraper(scraping_threshold)

    def classify_mud_file(self, filename: str) -> MudClassificationResult:
        """
        Classifies device type that the specified mud file describes.
        :param filename: Filename of the mud file.
        :return: Classified class and score
        """

        print("Classifying " + filename + "...")
        from mud.utilities import MUDUtilities

        return self.classify_mud_contents(MUDUtilities.get_mud_file_contents(filename))

    def classify_mud_contents(self, mud_file_contents: str) -> MudClassificationResult:
        '''
        Classifies device based on the contents of a mud file.
        :param mud_file_contents:
        :return: Classified class and score
        '''

        from mud.utilities import MUDUtilities
        from web_scraping.bing import BingSearchAPI
        from web_scraping.google import GoogleCustomSearchAPI

        systeminfo = MUDUtilities.get_systeminfo_from_mud_file(mud_file_contents)

        snippets = GoogleCustomSearchAPI.search_text(systeminfo)+BingSearchAPI.first_ten_snippets(systeminfo)

        classification_result = self.classifier.predict_snippets(snippets)

        return MudClassificationResult(classification_result.predicted_class, classification_result.prediction_probability)