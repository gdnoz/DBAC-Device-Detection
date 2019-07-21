class BacnetProfiler:
    """
    Takes a callable as input, which is in charge of simulating and querying the device.
    The text retrieved from running the callable is used for profiling.
    """

    def __init__(self, device_application_function: callable):
        self.application_function = device_application_function

    def run(self):
        from bacnet.classification import BacnetClassification
        from timeit import default_timer

        print("****************** Querying for Bacnet objects ******************")

        start = default_timer()

        query_result = self.application_function()

        print("************************ Query complete! ************************")

        bacnet_classification = BacnetClassification(0.2**2,0.2)

        classification_result = bacnet_classification.classify_bacnet_objects(query_result)

        end = default_timer()

        print("******************** Bacnet profiling result ********************")

        print("Device type:             " + classification_result.predicted_class)
        print("Classification score:    " + str(classification_result.score))
        print("Time:                    " + str(end-start))

        print(query_result)

        print("****************** Bacnet profiling completed *******************")

if __name__ == "__main__":
    from bacnet.local_device_applications.test_devices import arob,bacdrpc,bacri,bacrpc,bacsri,cdd3,cdrbac,src100,touchplateultra

    mud_profiler = BacnetProfiler(arob.run_application)
    #mud_profiler = BacnetProfiler(bacdrpc.run_application)
    #mud_profiler = BacnetProfiler(bacri.run_application)
    #mud_profiler = BacnetProfiler(bacrpc.run_application)
    #mud_profiler = BacnetProfiler(bacsri.run_application)
    #mud_profiler = BacnetProfiler(cdd3.run_application)
    #mud_profiler = BacnetProfiler(cdrbac.run_application)
    #mud_profiler = BacnetProfiler(src100.run_application)
    #mud_profiler = BacnetProfiler(touchplateultra.run_application)

    mud_profiler.run()