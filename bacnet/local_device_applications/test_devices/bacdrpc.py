'''
Based on: https://www.kele.com/Catalog/08%20Gas_Specialty_Sensors/PDFs/CDD3%20BACNET%20WALL%20INSTALLSHEET.pdf

CDD3 BACnet Room Carbon Dioxide Detector.

Simulates and queries device based on the above data sheet.
'''

def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''
    from bacpypes.object import AnalogInputObject,AnalogValueObject,BinaryValueObject,BinaryInputObject,BinaryOutputObject,MultiStateInputObject
    from bacnet.local_device_applications import SimulateAndQueryDeviceApplication
    import bacpypes.basetypes

    analog_input_objects =\
        [
        AnalogInputObject(
        objectIdentifier=('analogInput', 1),
        objectName='Temperature',
        objectType='analogInput',
        presentValue=19,
        description='Temperature',
        deviceType='Temperature Sensor',
        statusFlags=['inAlarm','inAlarm','inAlarm','inAlarm'],
        eventState='normal',
        reliability='noFaultDetected',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 2),
        objectName='Relative Humidity',
        objectType='analogInput',
        presentValue=60,
        description='Relative Humidity',
        deviceType='RH Sensor',
        statusFlags=['inAlarm','inAlarm','inAlarm','inAlarm'],
        eventState='normal',
        reliability='noFaultDetected',
        outOfService=False,
        units='percentRelativeHumidity'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 3),
        objectName='Dewpoint Temperature',
        objectType='analogInput',
        presentValue=8,
        description='Dewpoint Temperature',
        deviceType='Dewpoint Temperature Sensor',
        statusFlags=['inAlarm','inAlarm','inAlarm','inAlarm'],
        eventState='normal',
        reliability='noFaultDetected',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 4),
        objectName='Wet Bulb Temperature',
        objectType='analogInput',
        presentValue=19,
        description='Wet Bulb Temperature',
        deviceType='Wet Bulb Temperature Sensor',
        statusFlags=['inAlarm','inAlarm','inAlarm','inAlarm'],
        eventState='normal',
        reliability='noFaultDetected',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 5),
        objectName='Enthalpy',
        objectType='analogInput',
        presentValue=19,
        description='Enthalpy',
        deviceType='Enthalpy Sensor',
        statusFlags=['inAlarm','inAlarm','inAlarm','inAlarm'],
        eventState='normal',
        reliability='noFaultDetected',
        outOfService=False,
        units='kilojoulesPerKilogramDryAir'
    )]

    analog_value_objects = [
        AnalogValueObject(
            objectIdentifier=('analogValue', 1),
            objectName='Temperature Offset',
            objectType='analogValue',
            presentValue=0,
            description='Temperature Offset',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='deltaDegreesFahrenheit'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 2),
            objectName='RH Offset',
            objectType='analogValue',
            presentValue=0,
            description='RH Offset',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='percentRelativeHumidity'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 3),
            objectName='Atmospheric Pressure',
            objectType='analogValue',
            presentValue=1013,
            description='Atmospheric Pressure',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='hectopascals'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 4),
            objectName='Altitude',
            objectType='analogValue',
            presentValue=0,
            description='Altitude',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='feet'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 5),
            objectName='Display Mode',
            objectType='analogValue',
            presentValue=0,
            description='Display Mode',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='noUnits'
    )]

    binary_value_objects=[
        BinaryValueObject(
            objectIdentifier=('binaryValue', 1),
            objectName='Temperature Units',
            objectType='binaryValue',
            presentValue=0,
            description='Celsius (0) or Fahrenheit (1)',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        ), BinaryValueObject(
            objectIdentifier=('binaryValue', 2),
            objectName='Enthalpy Units',
            objectType='binaryValue',
            presentValue=0,
            description='kJ/kg (0) or BTU/lb (1)',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        )]

    objects = analog_input_objects+analog_value_objects+binary_value_objects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=381001, objectName="DP_001", objectType=8, systemStatus='operational', vendorName='Greystone Energy Systems',
                                                             vendorIdentifier=381, modelName='DP', firmwareRevision='1.2', applicationSoftwareVersion='1.0', description='Greystone Dewpoint Systems',
                                                             protocolVersion=1, protocolRevision=14, protocolObjectTypesSupported=['analogInput','analogValue','binaryValue','device'],
                                                             maxapdulength=128, segmentationSupported="noSegmentation", apduTimeout=6000, numberOfApduRetries=3, maxMaster=127, maxInfoFrames=1,
                                                             objects=objects)

if __name__ == "__main__":
    print(run_application())
    '''
    from multiprocessing.pool import ThreadPool
    import asyncio

    pool = ThreadPool(1)
    loop = asyncio.new_event_loop()
    result = pool.apply(run_application,args=())

    pool.close()
    pool.join()

    print(result.get())
    '''




