'''
Based on: http://ctsteknik.dk/upload_dir/shop/SN1.405-CDR-BAC.pdf

Simulates and queries device based on the above data sheet.
'''

def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''
    from bacpypes.object import AnalogInputObject,AnalogOutputObject,AnalogValueObject
    from bacnet.local_device_applications import SimulateAndQueryDeviceApplication
    import bacpypes.basetypes

    analog_input_objects =\
        [
        AnalogInputObject(
        objectName='Temperature Sensor',
        objectIdentifier=('analogInput', 0),
        objectType='analogInput',
        presentValue=21,
        #statusFlags='inAlarm',
        eventState='normal',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectName='Setpoint Adjust',
        objectIdentifier=('analogInput', 1),
        objectType='analogInput',
        presentValue=259,
        #statusFlags='inAlarm',
        eventState='normal',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectName='Humidity Sensor',
        objectIdentifier=('analogInput', 2),
        objectType='analogInput',
        presentValue=27,
        #statusFlags='inAlarm',
        eventState='normal',
        outOfService=False,
        units='percent'
    ), AnalogInputObject(
        objectName='RI1',
        objectIdentifier=('analogInput', 3),
        objectType='analogInput',
        presentValue=20981,
        #statusFlags='inAlarm',
        eventState='normal',
        outOfService=False,
        units='ohms'
    ), AnalogInputObject(
        objectName='RI2',
        objectIdentifier=('analogInput', 4),
        objectType='analogInput',
        presentValue=12841,
        #statusFlags='inAlarm',
        eventState='normal',
        outOfService=False,
        units='ohms'
    ), AnalogInputObject(
        objectName='CO2 Sensor',
        objectIdentifier=('analogInput', 5),
        objectType='analogInput',
        presentValue=738,
        #statusFlags='inAlarm',
        eventState='normal',
        outOfService=False,
        units='partsPerMillion'
    ), AnalogInputObject(
        objectName='LUX Sensor',
        objectIdentifier=('analogInput', 6),
        objectType='analogInput',
        presentValue=1974,
        #statusFlags='inAlarm',
        eventState='normal',
        outOfService=False,
        units='luxes'
    )]

    analog_output_objets = [AnalogOutputObject(
            objectIdentifier=('analogOutput',0),
            objectName='Y1',
            objectType='analogOutput',
            presentValue=72,
            eventState='normal',
            outOfService=False,
            units='percent'
    ), AnalogOutputObject(
            objectIdentifier=('analogOutput',1),
            objectName='Y2',
            objectType='analogOutput',
            presentValue=21,
            eventState='normal',
            outOfService=False,
            units='percent'
    ), AnalogOutputObject(
            objectIdentifier=('analogOutput',2),
            objectName='Y3',
            objectType='analogOutput',
            presentValue=82,
            eventState='normal',
            outOfService=False,
            units='percent'
    )]

    analog_value_objects = [AnalogValueObject(
        objectIdentifier=('analogValue',0),
        objectName='Temperature Setpoint',
        objectType='analogValue',
        presentValue=27,
        eventState='normal',
        outOfService=False,
        #relinquishDefault='Nonvol Temperature Setpoint'
    )]

    objects = analog_output_objets+analog_input_objects+analog_value_objects




    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=651000, objectName="CDR_001", objectType=8, systemStatus='operational', vendorName='SyxthSense',
                                                             vendorIdentifier=651, modelName='URD', protocolVersion=1, protocolRevision=10, maxapdulength=480,
                                                             segmentationSupported="noSegmentation", apduTimeout=3000, numberOfApduRetries=3, maxMaster=127, maxInfoFrames=1,
                                                             databaseRevision=0, objects=objects)

if __name__ == "__main__":
    print(run_application())