class MudClassification:
    """
    Given a MUD file as input, the file will be used to classify the type of the device.
    """

    def __init__(self):
        from Text_Classification.DeviceClassifier import DeviceClassifier
        self.classifier = DeviceClassifier(threshold=0.2)

    def classify_mud(self, filename: str) -> str:
        """
        Classifies device type that the specified mud file descirbes.
        :param filename: Filename of the mud file.
        :return: Classified class.
        """
        from MUD.MUDUtilities import MUDUtilities
        from MUD.URLRelevantTextScraper import URLRelevantTextScraper
        return self.classifier.predict_text(URLRelevantTextScraper(MUDUtilities.get_all_urls_from_mud(filename)).extract_text_from_urls())


if __name__ == "__main__":
    import os

    mud_classifier = MudClassification()

    for filename in os.listdir("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/data/MUD_Files"):
        print()
        print(mud_classifier.classify_mud(filename))
        print()