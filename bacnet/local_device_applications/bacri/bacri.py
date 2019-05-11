'''
Based on: http://www.syxthsense.com/product/product_pdf/MOD3.101-BAC-RI.pdf

Room Controller

Simulates and queries device based on the above data sheet.
'''

def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''
    from bacpypes.object import AnalogInputObject,AnalogOutputObject,AnalogValueObject,BinaryValueObject,BinaryInputObject,BinaryOutputObject,MultiStateInputObject
    from bacnet.local_device_applications import SimulateAndQueryDeviceApplication
    from random import randint

    analog_input_objects = [
        AnalogInputObject(
        objectIdentifier=('analogInput', 0),
        objectName='Sensor_Temperature',
        objectType='analogInput',
        presentValue=randint(0,150),
        eventState='normal',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 1),
        objectName='Setpoint_Adjust',
        objectType='analogInput',
        presentValue=randint(0,150),
        eventState='normal',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 2),
        objectName='Sensor_Humidity',
        objectType='analogInput',
        presentValue=randint(0,100),
        eventState='normal',
        outOfService=False,
        units='percent'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 3),
        objectName='RI1',
        objectType='analogInput',
        presentValue=randint(0,50000),
        eventState='normal',
        outOfService=False,
        units='ohms'
    ), AnalogInputObject(
        objectIdentifier=('analogInput', 4),
        objectName='User_Fan_Speed',
        objectType='analogInput',
        presentValue=randint(0,100),
        eventState='normal',
        outOfService=False,
        units='noUnits'
    )]

    analog_output_objects = [
        AnalogOutputObject(
            objectIdentifier=('analogOutput', 0),
            objectName='Y1',
            objectType='analogOutput',
            presentValue=randint(0, 100),
            eventState='normal',
            outOfService=False,
            units='percent'
        )
    ]

    analog_value_objects = [
        AnalogValueObject(
            objectIdentifier=('analogValue', 0),
            objectName='Setpoint_Temperature',
            objectType='analogValue',
            presentValue=randint(0, 100),
            eventState='normal',
            outOfService=False,
            units='degreesCelsius',
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 1),
            objectName='Fan_Speed',
            objectType='analogValue',
            presentValue=randint(0, 10),
            eventState='normal',
            outOfService=False,
            units='noUnits',
    ), AnalogValueObject(
            objectIdentifier=('analogValue', 2),
            objectName='Alarm_Code',
            objectType='analogValue',
            presentValue=randint(0, 100),
            eventState='normal',
            outOfService=False,
            units='noUnits',
    )]

    binary_input_objects = [
        BinaryInputObject(
        objectIdentifier=('binaryInput', 0),
        objectName='DI1',
        objectType='binaryInput',
        presentValue=randint(0,1),
        eventState='normal',
        outOfService=False,
        polarity='normal',
        activeText='on',
        inactiveText='off'
    ), BinaryInputObject(
        objectIdentifier=('binaryInput', 1),
        objectName='Operating_Mode',
        objectType='binaryInput',
        presentValue=randint(0, 1),
        eventState='normal',
        outOfService=False,
        polarity='normal',
        activeText='on',
        inactiveText='off'
    )]

    binary_output_ojects =[
        BinaryOutputObject(
            objectIdentifier=('binaryOutput', 0),
            objectName='DO1',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        ), BinaryOutputObject(
            objectIdentifier=('binaryOutput', 1),
            objectName='DO2',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        ), BinaryOutputObject(
            objectIdentifier=('binaryOutput', 2),
            objectName='Heating Symbol',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        ), BinaryOutputObject(
            objectIdentifier=('binaryOutput', 3),
            objectName='Cooling Symbol',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        ), BinaryOutputObject(
            objectIdentifier=('binaryOutput', 4),
            objectName='Open Arrow Symbol',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        ), BinaryOutputObject(
            objectIdentifier=('binaryOutput', 5),
            objectName='Close Arrow Symbol',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        ), BinaryOutputObject(
            objectIdentifier=('binaryOutput', 6),
            objectName='Day/Night Model',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        ), BinaryOutputObject(
            objectIdentifier=('binaryOutput', 7),
            objectName='SPA Reset',
            objectType='binaryOutput',
            presentValue=randint(0, 1),
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
        )]


    objects = analog_input_objects+analog_output_objects+analog_value_objects+binary_input_objects+binary_output_ojects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=651000, objectName="RIU_001", objectType=8, systemStatus='operational', vendorName='SyxthSense',
                                                             vendorIdentifier=651, modelName='RI', protocolVersion=1, protocolRevision=10, maxapdulength=480, segmentationSupported="noSegmentation",
                                                             apduTimeout=3000, numberOfApduRetries=3, maxMaster=127, maxInfoFrames=1,
                                                             objects=objects)

if __name__ == "__main__":
    print(run_application())