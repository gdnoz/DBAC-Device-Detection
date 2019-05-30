from mud.classification import MudClassification
from mud.utilities import MUDUtilities
import constants,os

def local_test(threshold: float):
    mud_classifier = MudClassification(threshold, 0.0)

    #["Tplink Camera.json","Ring doorbell.json","BlipcareBP meter.json"]:
    #os.listdir(constants.MUDFILES_DIR)
    for filename in ["Belkin Camera.json","Samsung Smart.json"]:
        result = mud_classifier.classify_mud_file(filename)
        print("FINAL PREDICTION: " + str(result.predicted_class) + ": " + str(result.score))

def synthetic_test_set_test(threshold: float, scraping_threshold: float):
    '''
    Tests the classification of MUD files using the set of test mud files specified in data/mud_synthetic_test_set.csv
    :param threshold: threshold to be used for the mud classification.
    :return:
    '''

    mud_classifier = MudClassification(threshold,scraping_threshold)

    numberOfTests = 0
    correctClassifications = 0
    scoreSum = 0.0
    noClassifications = 0

    with open(os.path.join(constants.DATA_DIR, "mud_synthetic_test_set.csv"), "r") as f:
        for line in f:
            numberOfTests += 1

            split = line.split(",")

            mud_url = split[0]
            correctClassification = split[1].rstrip()

            mud_file_from_web = MUDUtilities.get_mud_file(mud_url)

            classification_result = mud_classifier.classify_mud_contents(mud_file_from_web)

            classification = classification_result.predicted_class
            score = classification_result.score

            if classification == correctClassification:
                correctClassifications += 1
                scoreSum += score
                print(mud_url + ": " + "pass" + " (" + classification + ", " + str(score) + ")")
                continue
            elif classification == "No_classification":
                noClassifications += 1

            print(mud_url + ": " + "fail" + " (" + classification + ", " + str(score) + ")")

    print("****************** TEST COMPLETE: c_tresh: " + str(threshold)+ " s_threshold: " + str(scraping_threshold) + " ******************")
    print("Accuracy:                    " + str(float(correctClassifications/numberOfTests)))
    print("No device_classification:    " + str(float(noClassifications/numberOfTests)))
    print("Average score:               " + str(float(scoreSum/numberOfTests)))

def single_test(mud_url: str,threshold: float, scraping_threshold: float, correctClassification: str):
    mud_classifier = MudClassification(threshold, scraping_threshold)

    mud_file_from_web = MUDUtilities.get_mud_file(mud_url)

    classification_result = mud_classifier.classify_mud_contents(mud_file_from_web)

    classification = classification_result.predicted_class
    score = classification_result.score

    if classification == correctClassification:
        print(mud_url + ": " + "pass" + " (" + classification + ", " + str(score) + ")")
    else:
        print(mud_url + ": " + "fail" + " (" + classification + ", " + str(score) + ")")

if __name__ == "__main__":
    #single_test("https://iotanalytics.unsw.edu.au/mud/tplinkcameraMud.json",0.2,0.1,"Speaker")
    #single_test("https://iotanalytics.unsw.edu.au/mud/NetatmoWeatherStationMud.json", 0.2, 0.1, "Speaker")
    #single_test("https://iotanalytics.unsw.edu.au/mud/samsungsmartcamMud.json", 0.2, 0.1, "Speaker")
    #single_test("https://iotanalytics.unsw.edu.au/mud/belkincameraMud.json", 0.2, 0.1, "MediaPlayer")
    #single_test("https://iotanalytics.unsw.edu.au/mud/chromecastUltraMud.json", 0.2, 0.1, "MediaPlayer")

    #synthetic_test_set_test(0.2, 0.1) #best for non cumulative scoring
    synthetic_test_set_test(0.2, 0.1) #best for cumulative scoring
    #local_test(0.2,0.1)

    #for c_thresh in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
    #    for s_thresh in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
    #        synthetic_test_set_test(c_thresh,s_thresh)
