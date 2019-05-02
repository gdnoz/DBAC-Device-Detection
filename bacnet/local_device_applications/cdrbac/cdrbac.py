'''
Based on: http://ctsteknik.dk/upload_dir/shop/SN1.405-CDR-BAC.pdf

Simulates and queries device based on the above data sheet.
'''

def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''
    from bacpypes.object import AnalogInputObject
    from bacnet.local_device_applications import SimulateAndQueryDeviceApplication
    import bacpypes.basetypes

    objects =\
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

    '''
    Also add the proper device object properties. All naming is found under DeviceObject.py in object.py
    '''




    return SimulateAndQueryDeviceApplication.run_application(objectname="CDR_001", objectidentifier=651000, maxapdulength=480,
                                                             segmentationsupported="noSegmentation", vendoridentifier=651, objects=objects)

if __name__ == "__main__":
    print(run_application())