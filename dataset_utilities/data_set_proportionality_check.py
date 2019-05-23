def data_set_proportionality_check() -> dict:
    '''
    Checks the numer of words and unique words in each category for the data set.
    Used to check the proportionality of the classes.
    :return: Dict with results
    '''

    import os,constants,IOUtilities,json
    from collections import Counter

    result = dict()

    for (path,_,filenames) in list(os.walk(constants.DATA_SET_PATH))[1:]:
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

    return json.dumps(result,indent=4)

if __name__ == '__main__':
    import json
    print(data_set_proportionality_check())

