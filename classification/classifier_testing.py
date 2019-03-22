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


def test_naive_bayes(docs_to_train):
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
    print("******************************TESTING NB*******************************")
    print(metrics.classification_report(y_test, predicted,
                                        target_names=docs_to_train.target_names, labels=np.unique(predicted)))
    print("***********************************************************************")

def test_libsvm_svc(docs_to_train):
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
    print("******************************TESTING SVC******************************")
    print(metrics.classification_report(y_test, predicted,
                                        target_names=docs_to_train.target_names, labels=np.unique(predicted)))
    print("***********************************************************************")

class LemmaTokenizer(object):
    def __init__(self):
        from nltk.stem import WordNetLemmatizer
        self.wnl = WordNetLemmatizer()

    def __call__(self, articles):
        from nltk import word_tokenize
        return [self.wnl.lemmatize(t) for t in word_tokenize(articles)]

def test_libsvm_svc_2(docs_to_train):
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
    print("******************************TESTING SVC 2******************************")
    print(metrics.classification_report(y_test, predicted,
                                        target_names=docs_to_train.target_names, labels=np.unique(predicted)))
    print("***********************************************************************")


def test_sgd_classifier(docs_to_train):
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
    print("******************************TESTING SGD******************************")
    print(metrics.classification_report(y_test, predicted,
                                        target_names=docs_to_train.target_names, labels=np.unique(predicted)))
    print("***********************************************************************")

def test_logistic_regression(docs_to_train):
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
    print("******************************TESTING LR*******************************")
    print(metrics.classification_report(y_test, predicted,
                                        target_names=docs_to_train.target_names, labels=np.unique(predicted)))
    print("***********************************************************************")

def test_random_forrest(docs_to_train):
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
    print("************************TESTING Random Forrest****************************")
    print(metrics.classification_report(y_test, predicted,
                                        target_names=docs_to_train.target_names, labels=np.unique(predicted)))

if __name__ == "__main__":
    import constants
    dataset_path = constants.DATA_SET_PATH

    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = sklearn.datasets.load_files(dataset_path,
        description=None, categories=categories,
        load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
        docs_to_train.target, test_size=0.15)

    test_libsvm_svc(docs_to_train)
    test_libsvm_svc_2(docs_to_train)
    test_logistic_regression(docs_to_train)
    test_naive_bayes(docs_to_train)
    test_sgd_classifier(docs_to_train)
    test_random_forrest(docs_to_train)