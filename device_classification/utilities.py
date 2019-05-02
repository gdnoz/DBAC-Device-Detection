def run_tests_in_module_with_kfold_cross_validation(module_name: str):
    import constants,sys,os
    import numpy as np
    from inspect import getmembers, isfunction
    from sklearn.model_selection import train_test_split, KFold
    from sklearn.datasets import load_files


    average_result = dict()

    functions = [o for o in getmembers(sys.modules[module_name]) if isfunction(o[1]) and o[1].__module__ == module_name]

    for function in functions:
        dataset_path = constants.DATA_SET_PATH
        categories = [x[1] for x in os.walk(dataset_path)][0]

        docs_to_train = load_files(dataset_path, description=None, categories=categories,
                                   load_content=True, encoding='utf-8', shuffle=True, random_state=42)

        avg_results_for_func = list()
        kf = KFold(n_splits=8)

        for train_index, test_index in kf.split(docs_to_train.data):
            X_train, X_test = [docs_to_train.data[index] for index in train_index], [docs_to_train.data[index] for index in test_index]
            y_train, y_test = [docs_to_train.target[index] for index in train_index], [docs_to_train.target[index] for index in test_index]

            #X_train, X_test = docs_to_train.data[train_index], docs_to_train.data[test_index]
            #y_train, y_test = docs_to_train.target[train_index], docs_to_train.target[test_index]

            avg_results_for_func.append(function[1](docs_to_train, X_train, X_test, y_train, y_test)['weighted avg'])

        precision_avg = np.average([item['precision'] for item in avg_results_for_func])
        recall_avg = np.average([item['recall'] for item in avg_results_for_func])
        f1_score_avg = np.average([item['f1-score'] for item in avg_results_for_func])
        support = np.average([item['support'] for item in avg_results_for_func])

        average_result[function[0]] = {'precision avg': precision_avg, 'recall avg': recall_avg,
                                       'f1 score avg': f1_score_avg, 'support': support}

    print('{:30}'.format("test")+'{:15}'.format("precision avg")+'{:15}'.format("recall avg")+'{:15}'.format("f1 score avg") + '{:15}'.format("support"))

    for key,val in average_result.items():
        print('{:30}'.format(key)+'{:15}'.format(str(val['precision avg'])[:4])+'{:15}'.format(str(val['recall avg'])[:4])
              +'{:15}'.format(str(val['f1 score avg'])[:4])+'{:15}'.format(str(val['support'])[:4]))

def run_tests_in_module(module_name: str):
    import constants,sys,os
    import numpy as np
    from inspect import getmembers, isfunction
    from sklearn.model_selection import train_test_split, KFold
    from sklearn.datasets import load_files


    average_result = dict()

    functions = [o for o in getmembers(sys.modules[module_name]) if isfunction(o[1]) and o[1].__module__ == module_name]

    for function in functions:
        dataset_path = constants.DATA_SET_PATH
        categories = [x[1] for x in os.walk(dataset_path)][0]


        avg_results_for_func = list()
        for i in range(10):
            docs_to_train = load_files(dataset_path, description=None, categories=categories,
                                       load_content=True, encoding='utf-8', shuffle=True, random_state=42)

            X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
                                                                docs_to_train.target, test_size=0.15)

            avg_results_for_func.append(function[1](docs_to_train, X_train, X_test, y_train, y_test)['weighted avg'])

        precision_avg = np.average([item['precision'] for item in avg_results_for_func])
        recall_avg = np.average([item['recall'] for item in avg_results_for_func])
        f1_score_avg = np.average([item['f1-score'] for item in avg_results_for_func])
        support = np.average([item['support'] for item in avg_results_for_func])

        average_result[function[0]] = {'precision avg': precision_avg, 'recall avg': recall_avg,
                                       'f1 score avg': f1_score_avg, 'support': support}

    print('{:30}'.format("test")+'{:15}'.format("precision avg")+'{:15}'.format("recall avg")+'{:15}'.format("f1 score avg") + '{:15}'.format("support"))

    for key,val in average_result.items():
        print('{:30}'.format(key)+'{:15}'.format(str(val['precision avg'])[:4])+'{:15}'.format(str(val['recall avg'])[:4])
              +'{:15}'.format(str(val['f1 score avg'])[:4])+'{:15}'.format(str(val['support'])[:4]))
