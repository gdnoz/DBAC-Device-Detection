
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
from sklearn.metrics import accuracy_score, f1_score
from gensim.models import doc2vec,fasttext
import os,random

'''
https://github.com/ibrahimsharaf/doc2vec/blob/master/model.py
'''



def label_sentences(corpus, label_type):
    labeled = []
    for i, v in enumerate(corpus):
        label = label_type + '_' + str(i)
        labeled.append(doc2vec.LabeledSentence(v.split(), [label]))

    return labeled

def get_vectors(doc2vec_model, corpus_size, vectors_size, vectors_type):
    vectors = np.zeros((corpus_size, vectors_size))
    for i in range(0, corpus_size):
        prefix = vectors_type + '_' + str(i)
        vectors[i] = doc2vec_model.docvecs[prefix]
    return vectors

dataset_path = os.path.join(os.path.join(os.path.pardir,"data"),"dataset")

categories = [x[1] for x in os.walk(dataset_path)][0]

docs_to_train = sklearn.datasets.load_files(dataset_path,
    description=None, categories=categories,
    load_content=True, encoding='utf-8', shuffle=True, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
    docs_to_train.target, test_size=0.2)

x_train = label_sentences(X_train, 'Train')
x_test = label_sentences(X_test, 'Test')
corpus = x_train + x_test

print("Building Doc2Vec vocabulary")
d2v = doc2vec.Doc2Vec(min_count=1,  # Ignores all words with total frequency lower than this
                      window=10,  # The maximum distance between the current and predicted word within a sentence
                      vector_size=300,  # Dimensionality of the generated feature vectors
                      workers=5,  # Number of worker threads to train the model
                      alpha=0.025,  # The initial learning rate
                      min_alpha=0.00025,  # Learning rate will linearly drop to min_alpha as training progresses
                      dm=1)  # dm defines the training algorithm. If dm=1 means 'distributed memory' (PV-DM)
# and dm =0 means 'distributed bag of words' (PV-DBOW)
d2v.build_vocab(corpus)

ft = fasttext.FastText(min_count=1,  # Ignores all words with total frequency lower than this
                      window=10,  # The maximum distance between the current and predicted word within a sentence
                      workers=5,  # Number of worker threads to train the model
                      alpha=0.025,  # The initial learning rate
                      min_alpha=0.00025)  # Learning rate will linearly drop to min_alpha as training progresses


ft.build_vocab()


print("Training Doc2Vec model")
# 10 epochs take around 10 minutes on my machine (i7), if you have more time/computational power make it 20
for epoch in range(10):
    d2v.train(corpus, total_examples=d2v.corpus_count, epochs=d2v.epochs)
    ft.train(total_examples=ft.corpus_count, epochs=ft.epochs)
    # shuffle the corpus
    random.shuffle(corpus)
    # decrease the learning rate
    d2v.alpha -= 0.0002
    ft.alpha -= 0.0002
    # fix the learning rate, no decay
    d2v.min_alpha = d2v.alpha
    ft.min_alpha = ft.alpha

d2v.save("d2v.model")
ft.save("ft.model")


train_vectors = get_vectors(d2v, len(X_train), 300, 'Train')
train_vectors_1 = get_vectors(None, len(X_train), 300, 'Train')
model = SVC(kernel = 'linear', probability= True)
model.fit(train_vectors, np.array(y_train))
training_predictions = model.predict(train_vectors)

test_vectors = get_vectors(d2v, len(X_test), 300, 'Test')
predicted = model.predict(test_vectors)
print(metrics.classification_report(y_test, predicted, target_names=docs_to_train.target_names,labels=np.unique(predicted)))