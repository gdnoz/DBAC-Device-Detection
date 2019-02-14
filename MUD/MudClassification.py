class MudClassification:
    """
    Given a MUD file as input, the file will be used to classify the type of the device.
    """

    def __init__(self):
        from Text_Classification.DeviceClassifier import DeviceClassifier
        self.classifier = DeviceClassifier()

    def classify_mud(self, filename):
        from MUD.MUDUtilities import MUDUtilities
        from Scraping.WebScrapingUtilities import WebScrapingUtilities

        print("Classifying " + filename + "...")
        urls = MUDUtilities.get_all_urls_from_mud(filename)
        text = ""

        for url in urls:
            #print("Getting text from " + url + "...")
            try:
                text += WebScrapingUtilities.extract_text_from_url(url,timeout=2)
            except Exception as e:
                #print(e)
                #print("Skiping...")

        return self.classifier.predict_text(text)


if __name__ == "__main__":
    import os

    mud_classifier = MudClassification()

    for filename in os.listdir("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/data/MUD_Files"):
        print(mud_classifier.classify_mud(filename))