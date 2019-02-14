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

    def predict_text(self, text: str):
        return self.labels[self.pipeline.predict([text])[0]]

if __name__ == "__main__":
    dc = DeviceClassifier()
    k = dc.predict_text("Chromecast device used for video and audio streaming")
    print(k)
