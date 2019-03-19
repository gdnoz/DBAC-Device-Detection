from mud.classification import MudClassification
import constants,os


if __name__ == "__main__":

    mud_classifier = MudClassification(0.6)

    #["Tplink Camera.json","Ring doorbell.json","BlipcareBP meter.json"]:
    #os.listdir(constants.MUDFILES_DIR)
    for filename in ["WeMo motion.json","Netatmo Weather.json","ihome smart plug.json"]:
        result = mud_classifier.classify_mud_file(filename)
        print("FINAL PREDICTION: " + str(result.predicted_class) + ": " + str(result.score))
