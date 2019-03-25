import numpy as np
import sklearn
from sklearn import datasets
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
import os


def test_naive_bayes(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    nb_classifier = MultinomialNB()

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', nb_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted), output_dict=True)

def test_libsvm_svc(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted), output_dict=True)

def test_sgd_classifier(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    sgd_classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42,verbose=1)


    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', sgd_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted), output_dict=True)

def test_logistic_regression(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    lr_classifier = LogisticRegression(random_state=42, solver='lbfgs', multi_class='multinomial')

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', lr_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted), output_dict=True)

def test_random_forrest(docs_to_train, X_train, X_test, y_train, y_test):
    from sklearn.ensemble import RandomForestClassifier

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', rf_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted), output_dict=True)

if __name__ == "__main__":
    from classification.utilities import run_tests_in_module

    run_tests_in_module(__name__)