import numpy as np
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics

'''
Various tests of different text classification.
'''

def test_tf(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(stop_words='english')
    svc_classifier = LinearSVC()

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tfidf(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = LinearSVC()

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
    svc_classifier = LinearSVC()

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tfidf_bigram(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(ngram_range=(1, 2),stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = LinearSVC()

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)
'''
def test_no_tfidf_bigram_char(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(analyzer='char',ngram_range=(1, 2), stop_words='english')
    svc_classifier = LinearSVC()

    text_clf = Pipeline([
        ('tfidf_vect', count_vectorizer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)
'''

class LemmaTokenizer(object):
    def __init__(self):
        from nltk.stem import WordNetLemmatizer
        self.wnl = WordNetLemmatizer()

    def __call__(self, articles):
        from nltk import word_tokenize
        return [self.wnl.lemmatize(t) for t in word_tokenize(articles)]

def test_tf_lemmatizer(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(tokenizer=LemmaTokenizer(), stop_words='english', strip_accents='unicode', lowercase=True)
    svc_classifier = LinearSVC()

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

def test_tfidf_lemmatizer(docs_to_train, X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer(tokenizer=LemmaTokenizer(), stop_words='english', strip_accents='unicode', lowercase=True)
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = LinearSVC()

    text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    text_clf.fit(X_train, y_train)

    predicted = text_clf.predict(X_test)
    return metrics.classification_report(y_test, predicted,target_names=docs_to_train.target_names, labels=np.unique(predicted),output_dict=True)

if __name__ == "__main__":
    from device_classification.utilities import run_tests_in_module_with_kfold_cross_validation,run_tests_in_module
    import constants,os

    run_tests_in_module_with_kfold_cross_validation(__name__,os.path.join(constants.DATA_DIR,"dataset_initial"))
    #run_tests_in_module(__name__,run_tests_in_module_with_kfold_cross_validation(__name__,os.path.join(constants.DATA_DIR,"dataset_initial")))