class DeviceClassifier:
    """
    Used for classifying the category of an input text relevant to a device.
    Requires pmml/vectorizer.pkl, pmml/transformer.pkl, pmml/classifier.pkl to be present.
    """

    def __init__(self, threshold: float):
        import constants,os
        from sklearn.externals import joblib
        from sklearn.pipeline import Pipeline

        with open(os.path.join(constants.PMML_DIR,"labels.txt"),"r") as f:
            self.labels = [x.rstrip() for x in f.readlines()]

        count_vectorizer_path = os.path.join(constants.PMML_DIR, "vectorizer.pkl")
        tfidf_transformer_path = os.path.join(constants.PMML_DIR, "transformer.pkl")
        classifier_path = os.path.join(constants.PMML_DIR, "classifier.pkl")

        self.pipeline = Pipeline([
            ('vect', joblib.load(count_vectorizer_path)),
            ('tfidf', joblib.load(tfidf_transformer_path)),
            ('clf', joblib.load(classifier_path))
        ])

        self.threshold = threshold

    def predict_text(self, text: str) -> (str,float):
        """
        Returns the predicted class of the text and the distance of the hyperplane of that class.
        :param text: Text to be classified.
        :return: (Class of text, hyperplane distance)
        """
        predict_proba = self.pipeline.predict_proba([text])[0]

        import operator
        class_index, prob = max(enumerate(predict_proba), key=operator.itemgetter(1))

        if prob < self.threshold:
            return DeviceClassifier.DeviceClassificationResult("No_classification",0.0)
        else:
            return DeviceClassifier.DeviceClassificationResult(self.labels[class_index],prob)

    def predict_snippets(self, snippets: list, snippet_threshold: float, r2_scoring=True) -> (str,float):
        '''
        Each snippet is classified and the score is accumulated for each class.
        The highest scoring class is the returned classification.
        :param snippets: Text snippets from Google or Bing
        :return: DeviceClassificationResult
        '''

        from collections import Counter
        score_counter = Counter()

        for snippet in snippets:
            classification = self.predict_text(snippet)
            #print(snippet)
            #print(classification.predicted_class + " | " + str(classification.prediction_probability))

            if classification.prediction_probability >= snippet_threshold:
                if r2_scoring:
                    score_counter[classification.predicted_class] += classification.prediction_probability ** 2
                else:
                    score_counter[classification.predicted_class] += classification.prediction_probability

        print(score_counter)

        if len(score_counter) == 0:
            return DeviceClassifier.DeviceClassificationResult("No_classification", 0.0)

        most_common = score_counter.most_common(1)

        best_classification_score = most_common[0][1]
        best_classification = most_common[0][0]

        if best_classification_score > self.threshold and best_classification is not "":
            return DeviceClassifier.DeviceClassificationResult(best_classification, best_classification_score)
        else:
            return DeviceClassifier.DeviceClassificationResult("No_classification", 0.0)

    class DeviceClassificationResult:
        """
        Represents a device_classification result, containing the predicted class and a score of the prediction (accuracy).
        """

        predicted_class = ""
        prediction_probability = 0.0

        def __init__(self, predicted_class: str, prediction_probability: float):
            self.predicted_class = predicted_class
            self.prediction_probability = prediction_probability