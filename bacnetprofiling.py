class BacnetProfiler:
    """
    Takes a callable as input, which is in charge of simulating and querying the device.
    The text retrieved from running the callable is used for profiling.
    """

    def __init__(self, device_application_function: callable):
        self.application_function = device_application_function

    def run(self):
        from bacnet.classification import BacnetClassification

        print("****************** Querying for Bacnet objects ******************")

        query_result = self.application_function()

        print("************************ Query complete! ************************")

        bacnet_classification = BacnetClassification(0.2,0.1)

        classification_result = bacnet_classification.classify_bacnet_objects(query_result)

        print("******************** Bacnet profiling result ********************")

        print("Device type:             " + classification_result.predicted_class)
        print("Classification score:    " + str(classification_result.score))

        print("****************** Bacnet profiling completed *******************")

if __name__ == "__main__":
    from bacnet.local_device_applications.cdrbac import cdrbac
    from bacnet.local_device_applications.touchplateultra import touchplateultra
    mud_profiler = BacnetProfiler(cdrbac.run_application)
    #mud_profiler = BacnetProfiler(touchplateultra.run_application)
    mud_profiler.run()