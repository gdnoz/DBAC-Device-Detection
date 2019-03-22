if __name__ == "__main__":
    from classification.text_classification import DeviceClassifier

    prediction = DeviceClassifier(0.2).predict_text("Secondary Room Temperature Low Range when Temperature is configured to read through ADC ")

    print(prediction.predicted_class)
    print(prediction.prediction_probability)