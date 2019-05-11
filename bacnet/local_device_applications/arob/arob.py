
'''
Based on: http://www.neptronic.com/Controls/IAQController/PDF/AROB-BACnet%20Guide_170920.pdf

Universal Room Controller

Simulates and queries device based on the above data sheet.
'''

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

if __name__ == "__main__":
    print(run_application())