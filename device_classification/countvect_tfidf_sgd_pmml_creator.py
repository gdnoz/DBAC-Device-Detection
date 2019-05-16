def plot_decision_plane(docs_to_train, classifier):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import SGDClassifier

    colors = "bry"

    X = docs_to_train.data[:, :2]
    y = docs_to_train.target

    h = .02

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    cs = plt.contourf(xx, yy, Z, cmap=plt.cm.get_cmap("Paired"))
    plt.axis('tight')

    # Plot also the training points
    for i, color in zip(classifier.classes_, colors):
        idx = np.where(y == i)
        plt.scatter(X[idx, 0], X[idx, 1], c=color, label=docs_to_train.target_names[i],
                    cmap=plt.cm.get_cmap("Paired"), edgecolor='black', s=20)
    plt.title("Decision surface of multi-class SGD")
    plt.axis('tight')

    # Plot the three one-against-all classifiers
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    coef = classifier.coef_
    intercept = classifier.intercept_

    def plot_hyperplane(c, color):
        def line(x0):
            return (-(x0 * coef[c, 0]) - intercept[c]) / coef[c, 1]

        plt.plot([xmin, xmax], [line(xmin), line(xmax)],
                 ls="--", color=color)

    for i, color in zip(classifier.classes_, colors):
        plot_hyperplane(i, color)
    plt.legend()
    plt.show()

import sklearn
import numpy as np
from glob import glob
from sklearn import datasets
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics

from sklearn2pmml.pipeline import PMMLPipeline
from sklearn2pmml import sklearn2pmml


import os

dataset_path = os.path.join(os.path.join(os.path.pardir,"data"),"dataset")

categories = [x[1] for x in os.walk(dataset_path)][0]

docs_to_train = sklearn.datasets.load_files(dataset_path,
    description=None, categories=categories,
    load_content=True, encoding='utf-8', shuffle=True, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
    docs_to_train.target, test_size=0.01)

count_vectorizer = CountVectorizer(stop_words='english')
tfidf_transformer = TfidfTransformer(use_idf=True)
#classifier = SGDClassifier(loss='log', penalty='l2', alpha=1e-3, random_state=42,verbose=1)
classifier = SVC(kernel = 'linear', probability=True)



text_clf = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer),
        ('clf', classifier)
     ])


text_clf.fit(X_train,y_train)

#predicted = text_clf.predict(X_test)

#print(metrics.classification_report(y_test, predicted,
#    target_names=docs_to_train.target_names,labels=np.unique(predicted)))



#plot_decision_plane(docs_to_train, sgd_classifier)
import constants
from sklearn.externals import joblib

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

#print(pmml_pipeline.active_fields)
#print(pmml_pipeline.target_fields)

#sklearn2pmml(pmml_pipeline, "cv_tfidf_sgd.pmml", with_repr = True)

