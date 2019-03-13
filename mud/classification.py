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

    from typing import Type

    def __init__(self, threshold):
        from classification.text_classification import DeviceClassifier
        self.threshold = threshold
        self.classifier = DeviceClassifier(threshold=threshold)

    def classify_mud_file(self, filename: str) -> MudClassificationResult:
        """
        Classifies device type that the specified mud file describes.
        :param filename: Filename of the mud file.
        :return: Classified class.
        """

        print("Classifying " + filename + "...")
        from mud.utilities import MUDUtilities

        return self.classify_mud_contents(MUDUtilities.get_mud_file_contents(filename))

    def classify_mud_contents(self, mud_file_contents: str) -> MudClassificationResult:
        from mud.scraping import RelevantTextScraper
        from mud.utilities import MUDUtilities
        from scraping.bing import BingSearchAPI

        print("Classifying mud file...")

        mud_file_urls = MUDUtilities.get_all_urls_from_mud(mud_file_contents)
        text_from_mud_urls = RelevantTextScraper(mud_file_urls).extract_text_from_urls()

        print("Classifying based on mud URLs")
        classification_result = self.classifier.predict_text(text_from_mud_urls)

        if classification_result.prediction_probability > self.threshold and classification_result.predicted_class is not "":
            return MudClassificationResult(classification_result.predicted_class, classification_result.prediction_probability)

        systeminfo = MUDUtilities.get_systeminfo_from_mud_file(mud_file_contents)
        print("Classifying based on: " + systeminfo)

        urls = BingSearchAPI.first_ten_results(systeminfo)

        text_from_urls = RelevantTextScraper(set(urls)).extract_text_from_urls()

        classification_result = self.classifier.predict_text(text_from_urls)

        if classification_result.prediction_probability > self.threshold and classification_result.predicted_class is not "":
            return MudClassificationResult(classification_result.predicted_class,classification_result.prediction_probability)
        else:
            return MudClassificationResult("No_classification",0.0)