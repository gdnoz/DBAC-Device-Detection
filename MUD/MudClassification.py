class MudClassification:
    """
    Given a MUD file as input, the file will be used to classify the type of the device.
    """

    def __init__(self, threshold):
        from Text_Classification.DeviceClassifier import DeviceClassifier
        self.threshold = threshold
        self.classifier = DeviceClassifier(threshold=threshold)

    def classify_mud(self, filename: str) -> str:
        """
        Classifies device type that the specified mud file describes.
        :param filename: Filename of the mud file.
        :return: Classified class.
        """

        print("Classifying " + filename + "...")
        from MUD.MUDUtilities import MUDUtilities
        from MUD.URLRelevantTextScraper import URLRelevantTextScraper
        from Scraping.BingSearchAPI import BingSearchAPI

        text_from_mud_urls = URLRelevantTextScraper(MUDUtilities.get_all_urls_from_mud(filename)).extract_text_from_urls()

        print("Classifying based on MUD URLs")
        possible_result = self.classifier.predict_text(text_from_mud_urls)

        if possible_result.prediction_probability > self.threshold and possible_result.predicted_class is not "":
            return possible_result.predicted_class

        systeminfo = MUDUtilities.get_systeminfo_from_mud_file(filename)
        print("Classifying based on: " + systeminfo)

        urls = BingSearchAPI.first_ten_results(systeminfo)

        text_from_urls = URLRelevantTextScraper(set(urls)).extract_text_from_urls()

        possible_result = self.classifier.predict_text(text_from_urls)

        if possible_result.prediction_probability > self.threshold and possible_result.predicted_class is not "":
            return possible_result.predicted_class

        return "No_classification"