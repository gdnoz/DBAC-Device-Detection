import numpy as np
import matplotlib.pyplot as plt
import os,constants

from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

def plot_confusion_matrix(y_true, y_pred, classes, title,cmap=plt.cm.Blues):
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j]),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

def mud_matrix():
    classes = ["Alarm", "Camera", "Doorbell", "ElectricControl", "HealthMonitor", "HouseEnvironmentMonitor",
               "IndustryController", "IndustryEnvironmentSensor", "Light", "MediaPlayer", "MotionSensor", "Speaker","No_Classification"]

    labels = [i for i in range(len(classes))]

    y_true = [classes.index("Speaker"),
              classes.index("Doorbell"),
              classes.index("IndustryEnvironmentSensor"),
              classes.index("Camera"),
              classes.index("HealthMonitor"),
              classes.index("Camera"),
              classes.index("MediaPlayer"),
              classes.index("Camera"),
              classes.index("Light"),
              classes.index("ElectricControl"),
              classes.index("Light"),
              classes.index("HouseEnvironmentMonitor"),
              classes.index("Camera"),
              classes.index("HouseEnvironmentMonitor"),
              classes.index("Doorbell"),
              classes.index("Camera"),
              classes.index("Camera"),
              classes.index("ElectricControl"),
              classes.index("Speaker"),
              classes.index("MotionSensor"),
              classes.index("ElectricControl"),
              classes.index("Camera"),
              classes.index("HealthMonitor"),
              classes.index("HealthMonitor")]

    y_pred = [classes.index("Speaker"),
              classes.index("Doorbell"),
              classes.index("IndustryEnvironmentSensor"),
              classes.index("No_Classification"),
              classes.index("HealthMonitor"),
              classes.index("Camera"),
              classes.index("Speaker"),
              classes.index("Camera"),
              classes.index("Light"),
              classes.index("ElectricControl"),
              classes.index("Light"),
              classes.index("HouseEnvironmentMonitor"),
              classes.index("Camera"),
              classes.index("HouseEnvironmentMonitor"),
              classes.index("Doorbell"),
              classes.index("Camera"),
              classes.index("Camera"),
              classes.index("ElectricControl"),
              classes.index("Speaker"),
              classes.index("ElectricControl"),
              classes.index("ElectricControl"),
              classes.index("HealthMonitor"),
              classes.index("HealthMonitor"),
              classes.index("HealthMonitor")]

    plot_confusion_matrix(np.array(y_true),np.array(y_pred),np.array(classes),"mud_matrix")

    plt.savefig(os.path.join(os.path.join(constants.TEST_PATH,"confusion_matrices"),"confusion_matrix.png"))

def bacnet_matrix():
    pass

if __name__ == "__main__":
    np.set_printoptions(precision=2)

    mud_matrix()


