import warnings
import warnings

import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

import constants
import os

'''
Various tests of parameters for different classifiers using gridsearch.
'''

def tune_linear_svc():
    from sklearn.svm import LinearSVC

    warnings.filterwarnings("ignore")

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    svc_classifier = LinearSVC(max_iter=5000)

    mlp_pipeline = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', svc_classifier)
    ])

    dataset_path = constants.DATA_SET_PATH
    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = load_files(dataset_path, description=None, categories=categories,
                               load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    params = {'clf__C': [1.0,10.0,100.0,1000.0,10000.0,100000.0,1000000.0,10000000.0], 'clf__tol': [1e-6,1e-5,1e-4,1e-3,1e-2,1e-1]}

    gs = GridSearchCV(mlp_pipeline, params, cv=8,
                      n_jobs=-1, scoring='accuracy')
    gs.fit(docs_to_train.data, docs_to_train.target)

    plot_grid_search(gs.cv_results_, params['clf__C'], params['clf__tol'], 'C',
                     'Tol', 'linear_svc.png',x_log_scale=True)

def tune_random_forrest():
    from sklearn.ensemble import RandomForestClassifier

    warnings.filterwarnings("ignore")

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    rf_classifier = RandomForestClassifier(random_state=0)


    mlp_pipeline = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', rf_classifier)
    ])

    dataset_path = constants.DATA_SET_PATH
    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = load_files(dataset_path, description=None, categories=categories,
                               load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    params = {'clf__n_estimators': range(10, 100, 10), 'clf__max_depth': [None] + list(range(5, 11, 1))}

    gs = GridSearchCV(mlp_pipeline, params, cv=8,
                      n_jobs=-1, scoring='accuracy')
    gs.fit(docs_to_train.data, docs_to_train.target)

    plot_grid_search(gs.cv_results_, params['clf__n_estimators'], params['clf__max_depth'], 'N Estimators',
                     'Max Depth', 'rf.png')

def tune_xgboost():
    from xgboost import XGBClassifier

    warnings.filterwarnings("ignore")

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    xgb_classifier = XGBClassifier(random_state=0)

    mlp_pipeline = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', xgb_classifier)
    ])

    dataset_path = constants.DATA_SET_PATH
    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = load_files(dataset_path, description=None, categories=categories,
                               load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    params = {'clf__n_estimators': range(10, 200, 10), 'clf__max_depth':
        list(range(1, 11, 1))}

    gs = GridSearchCV(mlp_pipeline,params, cv=8,n_jobs=-1, scoring='accuracy')
    gs.fit(docs_to_train.data, docs_to_train.target)

    plot_grid_search(gs.cv_results_, params['clf__n_estimators'], params['clf__max_depth'], 'N Estimators','Max Depth', 'xgboost.png')


def tune_mlp():
    from sklearn.neural_network import MLPClassifier

    warnings.filterwarnings("ignore")

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)
    mlp_classifier = MLPClassifier()

    mlp_pipeline = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', mlp_classifier)
    ])

    dataset_path = constants.DATA_SET_PATH
    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = load_files(dataset_path, description=None, categories=categories,
                               load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    param = {'clf__alpha' : [1e-1,1e-2,1e-3,1e-4,1e-5,1e-6,1e-7], 'clf__max_iter' : range(50,500,50)}

    gs = GridSearchCV(mlp_pipeline, param, cv=8, n_jobs=-1, scoring='accuracy')
    gs.fit(docs_to_train.data,docs_to_train.target)

    plot_grid_search(gs.cv_results_,param['clf__alpha'],param['clf__max_iter'],'Alpha','Max Iterations','mlp.png',x_log_scale=True)


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

    plt.savefig("classifier_pngs/"+figname)

if __name__ == "__main__":
    #tune_linear_svc()
    #tune_mlp()
    #tune_random_forrest()
    tune_xgboost()
