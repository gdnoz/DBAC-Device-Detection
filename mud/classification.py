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
        from classificationcreation.text_classification import DeviceClassifier
        self.threshold = threshold
        self.classifier = DeviceClassifier(threshold=threshold)

    def classify_mud(self, filename: str) -> MudClassificationResult:
        """
        Classifies device type that the specified mud file describes.
        :param filename: Filename of the mud file.
        :return: Classified class.
        """

        print("Classifying " + filename + "...")
        from mud.utilities import MUDUtilities
        from mud.scraping import URLRelevantTextScraper
        from scraping.bing import BingSearchAPI

        text_from_mud_urls = URLRelevantTextScraper(MUDUtilities.get_all_urls_from_mud(filename)).extract_text_from_urls()

        print("Classifying based on mud URLs")
        possible_result = self.classifier.predict_text(text_from_mud_urls)

        if possible_result.prediction_probability > self.threshold and possible_result.predicted_class is not "":
            return MudClassificationResult(possible_result.predicted_class, possible_result.prediction_probability)

        systeminfo = MUDUtilities.get_systeminfo_from_mud_file(filename)
        print("Classifying based on: " + systeminfo)

        urls = BingSearchAPI.first_ten_results(systeminfo)

        text_from_urls = URLRelevantTextScraper(set(urls)).extract_text_from_urls()

        possible_result = self.classifier.predict_text(text_from_urls)

        if possible_result.prediction_probability > self.threshold and possible_result.predicted_class is not "":
            return MudClassificationResult(possible_result.predicted_class,possible_result.prediction_probability)

        return MudClassificationResult("No_classification",0.0)