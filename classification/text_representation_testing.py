import numpy as np
import sklearn
from sklearn import datasets
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer,TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
from inspect import getmembers, isfunction
import os,sys

def test_tf(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=False)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tfidf(docs_to_train, X_train, X_test, y_train, y_test):
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
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tf_bigram(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(ngram_range=(1, 2),stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=False)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tfidf_bigram(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(ngram_range=(1, 2),stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tf_bigram_char(docs_to_train, X_train, X_test, y_train, y_test):
    tfidf_vectorizer= TfidfVectorizer(analyzer='word',ngram_range=(1, 2),stop_words='english',use_idf=False)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('tfidf_vect', tfidf_vectorizer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tfidf_bigram_char(docs_to_train, X_train, X_test, y_train, y_test):
    ttfidf_vectorizer= TfidfVectorizer(analyzer='word',ngram_range=(1, 2),stop_words='english',use_idf=True)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('tfidf_vect', ttfidf_vectorizer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

class LemmaTokenizer(object):
    def __init__(self):
        from nltk.stem import WordNetLemmatizer
        self.wnl = WordNetLemmatizer()

    def __call__(self, articles):
        from nltk import word_tokenize
        return [self.wnl.lemmatize(t) for t in word_tokenize(articles)]

def test_tf_lemmatizer(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(tokenizer=LemmaTokenizer(), stop_words='english', strip_accents='unicode', lowercase=True)
    tfidf_transformer = TfidfTransformer(use_idf=False)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tfidf_lemmatizer(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(tokenizer=LemmaTokenizer(), stop_words='english', strip_accents='unicode', lowercase=True)
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = SVC(kernel='linear')

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

if __name__ == "__main__":
    from classification.utilities import run_tests_in_module
    run_tests_in_module(__name__)