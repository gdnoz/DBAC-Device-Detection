from bacnet.classification import BacnetClassification
import constants,os,sys,itertools,time,threading,queue
from bacnet.local_device_applications.test_devices import arob,bacdrpc,bacri,bacrpc,bacsri,cdd3,cdrbac,src100,touchplateultra
from inspect import getmembers, isfunction

def synthetic_test_set_test(threshold: float, scraping_threshold: float):
    bacnet_classifier = BacnetClassification(threshold, scraping_threshold)

    numberOfTests = 0
    correctClassifications = 0
    noClassifications = 0

    sys_modules = sys.modules
    test_device_modules = ['arob','bacdrpc','bacri','bacrpc','bacsri','cdd3','cdrbac','src100','touchplateultra']

    functions = {test_device_module:getmembers(sys_modules['bacnet.local_device_applications.test_devices.'+test_device_module])[-1][1]
                 for test_device_module in test_device_modules}

    bacnet_classification = BacnetClassification(0.2, 0.1)


    with open(os.path.join(constants.DATA_DIR, "bacnet_test_set.csv"), "r") as f:
        for line in f:
            device,correctClassification = line.split(',')

            function = functions[device]

            q = queue.Queue()

            thread = threading.Thread(function(q))
            thread.start()
            thread.join()

            classification_result = bacnet_classification.classify_bacnet_objects(q.get())

            classification = classification_result.predicted_class
            score = classification_result.score

            if classification == correctClassification:
                correctClassifications += 1
                print(device + ": " + "pass" + " (" + classification + ", " + str(score) + ")")
                continue
            elif classification == "No_classification":
                noClassifications += 1

    print("****************** TEST COMPLETE: c_tresh: " + str(threshold) + " s_thresh: " + str(scraping_threshold) + " ******************")
    print("Accuracy:            " + str(float(correctClassifications/numberOfTests)))
    print("No device_classification:   " + str(float(noClassifications/numberOfTests)))

if __name__ == "__main__":
    synthetic_test_set_test(0.2,0.1)
