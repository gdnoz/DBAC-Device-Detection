def data_set_proportionality_check(dataset_path: str) -> dict:
    '''
    Checks the numer of words and unique words in each category for the data set.
    Used to check the proportionality of the classes.
    :return: Dict with results
    '''

    import os,constants,IOUtilities,json
    from collections import Counter

    result = dict()

    for (path,_,filenames) in list(os.walk(dataset_path))[1:]:
        category = path.split("/")[-1]

        result.update({category:dict()})

        for filename in filenames:
            current_file_path = os.path.join(path,filename)
            current_file_content = IOUtilities.read_content_from_file(current_file_path)

            counter = Counter(current_file_content.split())

            no_unique_words = len(counter)
            no_words = sum([counter[key] for key in counter])

            if 'unique_words' not in result[category] and 'words' not in result[category]:
                result[category].update({'unique_words':no_unique_words})
                result[category].update({'words': no_words})
            else:
                result[category]['unique_words'] += no_unique_words
                result[category]['words'] += no_words

    return result

def create_bar_plot(unique_words,words,labels,title):
    import matplotlib.pyplot as plt
    plt.rcdefaults()
    import numpy as np
    import matplotlib.pyplot as plt

    y_pos = np.arange(len(labels))

    subplot = plt.subplot(111)

    bar1 = subplot.bar(y_pos,unique_words,width=0.4,color='b',align='center')
    bar2 = subplot.bar(y_pos+0.4, words, width=0.4, color='r', align='center')

    subplot.legend( (bar1[0],bar2[0]), ('Unique Words', 'Total Words') )

    plt.xticks(y_pos, labels, rotation='vertical')
    plt.subplots_adjust(bottom=0.45)

    plt.ylabel('Count')
    plt.title(title)

    plt.savefig("test.png")

if __name__ == '__main__':
    import constants,os

    res = data_set_proportionality_check(os.path.join(constants.DATA_DIR,"dataset_clean_tos"))

    labels = list()
    unique_words = list()
    words = list()

    for k,v in res.items():
        labels += [k]
        unique_words += [v['unique_words']]
        words += [v['words']]

    create_bar_plot(unique_words, words, labels, "TOS Training Dataset Word Distribution")

    #print(data_set_proportionality_check(constants.DATA_SET_PATH_TOS))

