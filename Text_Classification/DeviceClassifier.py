class DeviceClassifier:
    """
    Used for classifying the category of an input text relevant to a device.
    Requires pmml/vectorizer.pkl, pmml/transformer.pkl, pmml/classifier.pkl to be present.
    """

    def __init__(self):
        from sklearn.externals import joblib
        from sklearn.pipeline import Pipeline
        with open("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/Text_Classification/pmml/labels.txt","r") as f:
            self.labels = [x.rstrip() for x in f.readlines()]
        self.pipeline = Pipeline\
        ([
            ('vect', joblib.load("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/Text_Classification/pmml/vectorizer.pkl")),
            ('tfidf', joblib.load("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/Text_Classification/pmml/transformer.pkl")),
            ('clf', joblib.load("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/Text_Classification/pmml/classifier.pkl"))
        ])

    def predict_text(self, text: str) -> (str,float):
        """
        Returns the predicted class of the text and the distance of the hyperplane of that class.
        :param text: Text to be classified.
        :return: (Class of text, hyperplane distance)
        """
        class_index = self.pipeline.predict([text])[0]
        prob = self.pipeline.predict_proba([text])
        print(prob[0])

        return (self.labels[class_index],prob[0][class_index])

if __name__ == "__main__":
    import Scraping.WebScrapingUtilities
    dc = DeviceClassifier()
    k = dc.predict_text(Scraping.WebScrapingUtilities.WebScrapingUtilities.extract_text_from_url("https://www.ezviz.eu/wifi-cameras/c6b/",timeout=10))
    print(k)
