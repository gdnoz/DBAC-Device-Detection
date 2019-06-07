from sklearn.calibration import CalibratedClassifierCV

import constants,os
import sklearn
from sklearn import datasets
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn2pmml.pipeline import PMMLPipeline

'''
Creates the trained models, which then can be loaded and used for classification later.
'''

dataset_path = os.path.join(os.path.join(os.path.pardir,"data"),"dataset_clean_tos")

categories = [x[1] for x in os.walk(dataset_path)][0]

docs_to_train = sklearn.datasets.load_files(dataset_path,
    description=None, categories=categories,
    load_content=True, encoding='utf-8', shuffle=True, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
    docs_to_train.target, test_size=0.01)

count_vectorizer = CountVectorizer(stop_words='english')
tfidf_transformer = TfidfTransformer(use_idf=True)
classifier = SVC(kernel = 'linear', probability = True)

text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', classifier)
     ])

text_clf.fit(X_train,y_train)


try:
    os.remove(os.path.join(constants.PMML_DIR,"vectorizer.pkl"))
    os.remove(os.path.join(constants.PMML_DIR,"transformer.pkl"))
    os.remove(os.path.join(constants.PMML_DIR,"classifier.pkl"))
except Exception:
    pass

joblib.dump(count_vectorizer, os.path.join(constants.PMML_DIR,"vectorizer.pkl"))
joblib.dump(tfidf_transformer,os.path.join(constants.PMML_DIR,"transformer.pkl"))
joblib.dump(classifier, os.path.join(constants.PMML_DIR,"classifier.pkl"))

with open(os.path.join(constants.PMML_DIR,"labels.txt"),"w+") as f:
    f.write('\n'.join(docs_to_train.target_names))

loaded_count_vectorizer = joblib.load(os.path.join(constants.PMML_DIR,"vectorizer.pkl"))
loaded_tfidf_transformer = joblib.load(os.path.join(constants.PMML_DIR,"transformer.pkl"))
loaded_classifier = joblib.load(os.path.join(constants.PMML_DIR,"classifier.pkl"))

pmml_pipeline = PMMLPipeline([
        ('vect', loaded_count_vectorizer),
        ('tfidf', loaded_tfidf_transformer),
        ('clf', loaded_classifier)
     ])