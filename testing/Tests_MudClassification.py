from mud.classification import MudClassification
import constants,os


if __name__ == "__main__":

    mud_classifier = MudClassification(0.6)

    for filename in os.listdir(constants.MUDFILES_DIR):
        result = mud_classifier.classify_mud_file(filename)
        print("FINAL PREDICTION: " + str(result.predicted_class) + ": " + str(result.score))
