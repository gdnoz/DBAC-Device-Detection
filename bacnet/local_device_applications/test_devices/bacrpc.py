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
        objectName='Pressure_Sensor_Value',
        objectType='analogInput',
        presentValue=101325,
        description='Pressure Value in Pa or wc',
        deviceType='Room Pressure Sensor',
        statusFlags=['inAlarm','inAlarm','inAlarm','inAlarm'],
        eventState='normal',
        reliability='noFaultDetected',
        outOfService=False,
        units='pascals'
    )]

    analog_value_objects = [
        AnalogValueObject(
            objectIdentifier=('analogValue', 1),
            objectName='Pressure_Averaging_Time',
            objectType='analogValue',
            presentValue=5,
            description='Pressure Averaging Time',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='seconds'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 2),
            objectName='Alarm_High_Limit',
            objectType='analogValue',
            presentValue=0.5,
            description='Alarm High Limit in Pa or wc',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='pascals'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 3),
            objectName='Alarm_Low_Limit',
            objectType='analogValue',
            presentValue=-0.5,
            description='Alarm Low Limit in Pa or wc',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='pascals'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 4),
            objectName='Alarm_On_Delay',
            objectType='analogValue',
            presentValue=5,
            description='Alarm On Delay',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='minutes'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 5),
            objectName='Alarm_Off_Delay',
            objectType='analogValue',
            presentValue=5,
            description='Alarm Off Delay',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='minutes'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 6),
            objectName='Alarm_Silence_Time',
            objectType='analogValue',
            presentValue=30,
            description='Alarm Silence Time',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='minutes'
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 7),
            objectName='Buzzer_Volume',
            objectType='analogValue',
            presentValue=2,
            description='CO2 LCD Display Modes',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='noUnits'
    )]

    binary_value_objects=[
        BinaryValueObject(
            objectIdentifier=('binaryValue', 1),
            objectName='Alarm_Enable',
            objectType='binaryValue',
            presentValue=1,
            description='0 = Alarm Disable, 1 = Alarm Enable',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        ), BinaryValueObject(
            objectIdentifier=('binaryValue', 2),
            objectName='Alarm_Test',
            objectType='binaryValue',
            presentValue=0,
            description='0 = Normal Operation, 1 = Alarm Test',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        ), BinaryValueObject(
            objectIdentifier=('binaryValue', 3),
            objectName='Backlight_Enable',
            objectType='binaryValue',
            presentValue=1,
            description='0 = Backlight Disable, 1 = Backlight Enable',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        ), BinaryValueObject(
            objectIdentifier=('binaryValue', 4),
            objectName='Pressure_Units',
            objectType='binaryValue',
            presentValue=0,
            description='0 = wc, 1 = Pa ',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        ), BinaryValueObject(
            objectIdentifier=('binaryValue', 5),
            objectName='Pressure_Range',
            objectType='binaryValue',
            presentValue=1,
            description='0 = Low Pressure Range, 1 = High Pressure Range',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        )]

    binary_input_objects = [BinaryInputObject(
            objectIdentifier=('binaryInput',1),
            objectName='Alarm_Status',
            objectType='binaryInput',
            presentValue=0,
            description='Alarm Status',
            deviceType='0 = No Alarm, 1 = Pressure Alarm',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
    ), BinaryInputObject(
            objectIdentifier=('binaryInput',2),
            objectName='Low_Alarm_Status',
            objectType='binaryInput',
            presentValue=0,
            description='Low Alarm Status',
            deviceType='0 = No Low Alarm, 1 = Low Pressure Alarm',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
    ), BinaryInputObject(
            objectIdentifier=('binaryInput',3),
            objectName='High_Alarm_Status',
            objectType='binaryInput',
            presentValue=0,
            description='High Alarm Status',
            deviceType='0 = No High Alarm, 1 = High Pressure Alarm',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
    )]

    objects = analog_input_objects+analog_value_objects+binary_value_objects+binary_input_objects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=381003, objectName="Room Pressure Monitor 003", objectType=8, systemStatus='operational', vendorName='Greystone Energy Systems',
                                                             vendorIdentifier=381, modelName='RPC', firmwareRevision='1.4', applicationSoftwareVersion='1.0', description='Greystone RP Monitor',
                                                             protocolVersion=1, protocolRevision=7, protocolObjectTypesSupported=['analogInput','analogValue','binaryInput','binaryValue','device'],
                                                             maxapdulength=128, segmentationSupported="noSegmentation", apduTimeout=10000, numberOfApduRetries=3, maxMaster=127, maxInfoFrames=1,
                                                             objects=objects)

if __name__ == "__main__":
    print(run_application())