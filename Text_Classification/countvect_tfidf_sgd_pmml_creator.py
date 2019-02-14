import sklearn
import numpy as np
from glob import glob
from sklearn import datasets
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from sklearn2pmml.pipeline import PMMLPipeline
from sklearn2pmml import sklearn2pmml


import os

dataset_path = os.path.join(os.path.join(os.path.pardir,"data"),"dataset")

categories = [x[1] for x in os.walk(dataset_path)][0]

docs_to_train = sklearn.datasets.load_files(dataset_path,
    description=None, categories=categories,
    load_content=True, encoding='utf-8', shuffle=True, random_state=42)

#X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
#    docs_to_train.target, test_size=0.01)

count_vectorizer = CountVectorizer(stop_words='english')
tfidf_transformer = TfidfTransformer(use_idf=True)
sgd_classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42,verbose=1)


text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', sgd_classifier)
     ])

text_clf.fit(docs_to_train.data,docs_to_train.target)

from sklearn.externals import joblib

joblib.dump(count_vectorizer, "pmml/vectorizer.pkl")
joblib.dump(tfidf_transformer, "pmml/transformer.pkl")
joblib.dump(sgd_classifier, "pmml/classifier.pkl")

with open("pmml/labels.txt","w+") as f:
    f.write('\n'.join(docs_to_train.target_names))


loaded_count_vectorizer = joblib.load("pmml/vectorizer.pkl")
loaded_tfidf_transformer = joblib.load("pmml/transformer.pkl")
loaded_sgd_classifier = joblib.load("pmml/classifier.pkl")

pmml_pipeline = PMMLPipeline([
        ('vect', loaded_count_vectorizer),
        ('tfidf', loaded_tfidf_transformer),
        ('clf', loaded_sgd_classifier)
     ])

#print(pmml_pipeline.active_fields)
#print(pmml_pipeline.target_fields)

sklearn2pmml(pmml_pipeline, "cv_tfidf_sgd.pmml", with_repr = True)
