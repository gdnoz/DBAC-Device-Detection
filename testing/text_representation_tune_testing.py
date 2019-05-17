import warnings
import warnings

import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

import constants
import os


'''
Tests for tuning parameters of various text representations. Primarily tests of using different sizes of n-grams.
'''

def tune_tfidf_ngram():
    warnings.filterwarnings("ignore")

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = SVC()

    tdf_ngram = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    dataset_path = constants.DATA_SET_PATH
    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = load_files(dataset_path, description=None, categories=categories,
                               load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    param = {'vect__ngram_range' : [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)], 'clf__kernel':['linear']}

    gs = GridSearchCV(tdf_ngram, param, cv=8, n_jobs=-1, scoring='accuracy')
    gs.fit(docs_to_train.data,docs_to_train.target)

    plot_grid_search(gs.cv_results_,param['vect__ngram_range'],param['clf__kernel'],'n-gram range','kernel','tfidf.png')

def tune_tf_ngram():
    warnings.filterwarnings("ignore")

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=False)
    svc_classifier = SVC()

    tdf_ngram = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    dataset_path = constants.DATA_SET_PATH
    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = load_files(dataset_path, description=None, categories=categories,
                               load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    param = {'vect__ngram_range' : [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)], 'clf__kernel':['linear']}

    gs = GridSearchCV(tdf_ngram, param, cv=8, n_jobs=-1, scoring='accuracy')
    gs.fit(docs_to_train.data,docs_to_train.target)

    plot_grid_search(gs.cv_results_,param['vect__ngram_range'],param['clf__kernel'],'n-gram range','kernel','tf.png')

def plot_grid_search(cv_results, grid_param_1, grid_param_2, name_param_1, name_param_2,figname,x_log_scale=False,y_log_scale=False):
    import matplotlib.pyplot as plt

    scores_mean = cv_results['mean_test_score']
    scores_mean = np.array(scores_mean).reshape(len(grid_param_2),len(grid_param_1))

    scores_sd = cv_results['std_test_score']
    scores_sd = np.array(scores_sd).reshape(len(grid_param_2),len(grid_param_1))

    _, ax = plt.subplots(1,1)

    for idx, val in enumerate(grid_param_2):
        ax.plot(grid_param_1, scores_mean[idx,:], '-o', label= name_param_2 + ': ' + str(val))

    ax.set_title("Grid Search Scores", fontsize=20, fontweight='bold')
    ax.set_xlabel(name_param_1, fontsize=16)
    ax.set_ylabel('CV Average Score', fontsize=16)

    if x_log_scale:
        ax.set_xscale("log")

    if y_log_scale:
        ax.set_yscale("log")

    ax.legend(loc="best", fontsize=15)
    ax.grid('on')

    plt.savefig("representation_pngs/"+figname)

if __name__ == "__main__":
    #tune_tfidf_ngram()
    tune_tf_ngram()