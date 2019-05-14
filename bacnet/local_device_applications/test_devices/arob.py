
'''
Based on: http://www.neptronic.com/Controls/IAQController/PDF/AROB-BACnet%20Guide_170920.pdf

Universal Room Controller

Simulates and queries device based on the above data sheet.
'''
import queue
import threading
from queue import Queue


def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''
    from bacpypes.object import AnalogInputObject,AnalogOutputObject,AnalogValueObject,BinaryInputObject,BinaryOutputObject,MultiStateInputObject
    from bacnet.local_device_applications import SimulateAndQueryDeviceApplication
    import bacpypes.basetypes

    analog_input_objects = []

    analog_output_objets = []

    analog_value_objects = []

    binary_input_objects = []

    binary_output_objects = []

    multistate_input_objects = []

    objects = analog_output_objets+analog_input_objects+analog_value_objects+binary_input_objects+binary_output_objects+multistate_input_objects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=153000, objectName="AROB24TGVH", objectType='device', systemStatus='operational', vendorName='Neptronic',
                                                             vendorIdentifier=153, modelName='ARBGVH', firmwareRevision='1.06', applicationSoftwareVersion='1.27', protocolVersion=1, protocolRevision=14,
                                                             maxapdulength=480, segmentationSupported="noSegmentation", apduTimeout=3000, numberOfApduRetries=3,
                                                             protocolObjectTypesSupported=['analogInput','analogOutput','analogValue', 'binaryInput','binaryOutput','binaryValue','device','multiStateValue'],
                                                             maxMaster=127, maxInfoFrames=1, databaseRevision=0, objects=objects)

def run_for_thread(queue: Queue):
    result = run_application()
    queue.put(result)

if __name__ == "__main__":
    print(run_application())
    '''
    q = queue.Queue()

    thread = threading.Thread(run_for_thread(q))
    thread.start()
    thread.join()

    print(q.get())

    import time

    thread = threading.Thread(time.sleep(5))
    thread.start()
    thread.join()

    thread = threading.Thread(run_for_thread(q))
    thread.start()
    thread.join()

    print(q.get())
    '''