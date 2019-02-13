import sklearn
import numpy as np
from glob import glob
from sklearn import datasets
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix

import os

dataset_path = os.path.join(os.path.join(os.path.pardir,"data"),"dataset")

categories = [x[1] for x in os.walk(dataset_path)][0]

docs_to_train = sklearn.datasets.load_files(dataset_path,
    description=None, categories=categories,
    load_content=True, encoding='utf-8', shuffle=True, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
    docs_to_train.target, test_size=0.1)

"""
count_vect = CountVectorizer(stop_words='english')
X_train_counts = count_vect.fit(raw_documents=X_train)

tdfif_transformer = TfidfTransformer(use_idf=True)

X_train_tfidf = tdfif_transformer.fit_transform(X_train_counts)

count_vect = CountVectorizer(stop_words='english')
X_test_counts = count_vect.fit_transform(raw_documents=X_test)

tfidf_transformer = TfidfTransformer(use_idf=True)
X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts)
"""

text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
    ('tfidf', TfidfTransformer(use_idf=True)),
    ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42,
    verbose=1))])

text_clf.fit(X_train, y_train)

predicted = text_clf.predict(X_test)

print(metrics.classification_report(y_test, predicted,
    target_names=docs_to_train.target_names,labels=np.unique(predicted)))
