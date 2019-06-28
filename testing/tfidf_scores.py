import os,constants

import sklearn.datasets
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from collections import Counter
from wordcloud import WordCloud



def get_key_for_value(d: dict, value):
    return [k for k,v in d.items() if v == value][0]

if __name__=="__main__":
    dataset_path = os.path.join(os.path.join(os.path.pardir, "data"), "dataset_clean_tos")

    categories = [x[1] for x in os.walk(dataset_path)][0]

    docs_to_train = sklearn.datasets.load_files(dataset_path,
                                                description=None, categories=categories,
                                                load_content=True, encoding='utf-8', shuffle=True, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
                                                        docs_to_train.target, test_size=0.01)

    count_vectorizer_solo = CountVectorizer(stop_words='english')

    countvect_pipeline = Pipeline([
        ('vect', count_vectorizer_solo)
    ])

    count_vectorizer = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer(use_idf=True)

    tfidf_pipeline = Pipeline([
        ('vect', count_vectorizer),
        ('tfidf', tfidf_transformer)
    ])

    cv_trans = countvect_pipeline.fit_transform(X_train, y_train)
    tfidf_trans = tfidf_pipeline.fit_transform(X_train, y_train)

    target_names = docs_to_train.target_names

    cv_coo = cv_trans.tocoo()
    tfidf_coo = tfidf_trans.tocoo()

    category_counters = [(target_name, Counter()) for target_name in target_names]
    category_tfidf_counters = [(target_name, Counter()) for target_name in target_names]

    for document,int_word,tf_idf in zip(tfidf_coo.row, tfidf_coo.col, tfidf_coo.data):
        word = get_key_for_value(count_vectorizer.vocabulary_, int_word)
        category_tfidf_counters[y_train[document]][1][word] += tf_idf


    for document,int_word,occurence in zip(cv_coo.row, cv_coo.col, cv_coo.data):
        word = get_key_for_value(count_vectorizer_solo.vocabulary_,int_word)

        category_counters[y_train[document]][1][word] += occurence
    

    import matplotlib.pyplot as plt

    for (category,counter) in category_counters:
        category_text = ""
        for word,counter in counter.most_common(20):
            for i in range(counter):
                category_text += " " + word + " "

        wordcloud = WordCloud(repeat=False, collocations=False).generate(category_text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(os.path.join(constants.WORDCLOUDS_PATH,category+".png"))


    for (category, counter) in category_tfidf_counters:
        print(category)
        print(counter.most_common(20))






