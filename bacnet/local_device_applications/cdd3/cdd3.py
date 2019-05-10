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
    from bacpypes.object import AnalogInputObject,AnalogOutputObject,AnalogValueObject,BinaryInputObject,BinaryOutputObject,MultiStateInputObject
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

    analog_value_objects = [
        AnalogValueObject(
            objectIdentifier=('analogValue',0),
            objectName='Temperature Setpoint',
            objectType='analogValue',
            presentValue=27,
            eventState='normal',
            outOfService=False,
            units='degreesCelsius',
            relinquishDefault=20
    ), AnalogValueObject(
            objectIdentifier=('analogValue',1),
            objectName='Humidity Setpoint',
            objectType='analogValue',
            presentValue=12,
            eventState='normal',
            outOfService=False,
            units='percent',
            relinquishDefault=50
    ),  AnalogValueObject(
            objectIdentifier=('analogValue',2),
            objectName='CO2 Setpoint',
            objectType='analogValue',
            presentValue=502,
            eventState='normal',
            outOfService=False,
            units='partsPerMillion',
            relinquishDefault=500
    ), AnalogValueObject(
            objectIdentifier=('analogValue',3),
            objectName='LUX Setpoint',
            objectType='analogValue',
            presentValue=1129,
            eventState='normal',
            outOfService=False,
            units='luxes',
            relinquishDefault=1500
    ), AnalogValueObject(
            objectIdentifier=('analogValue',4),
            objectName='DI1 Pulse Count',
            objectType='analogValue',
            presentValue=8276491,
            eventState='normal',
            outOfService=False,
            units='noUnits',
            relinquishDefault=0
    ), AnalogValueObject(
            objectIdentifier=('analogValue',5),
            objectName='DI2 Pulse Count',
            objectType='analogValue',
            presentValue=292384,
            eventState='normal',
            outOfService=False,
            units='noUnits',
            relinquishDefault=0
    ), AnalogValueObject(
            objectIdentifier=('analogValue',6),
            objectName='LCD Backlight Brightness',
            objectType='analogValue',
            presentValue=7,
            eventState='normal',
            outOfService=False,
            units='noUnits',
            relinquishDefault=0
    ),
    ]

    binary_input_objects = [BinaryInputObject(
            objectIdentifier=('binaryInput',0),
            objectName='DI1',
            objectType='binaryInput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
    ), BinaryInputObject(
            objectIdentifier=('binaryInput',1),
            objectName='DI2',
            objectType='binaryInput',
            presentValue=1,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
    ), BinaryInputObject(
            objectIdentifier=('binaryInput',2),
            objectName='Occupancy',
            objectType='binaryInput',
            presentValue=1,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
    ), BinaryInputObject(
            objectIdentifier=('binaryInput',3),
            objectName='Push Button 1',
            objectType='binaryInput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
    ), BinaryInputObject(
            objectIdentifier=('binaryInput',4),
            objectName='Push Button 2',
            objectType='binaryInput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
    )]

    binary_output_objects = [BinaryOutputObject(
            objectIdentifier=('binaryOutput',0),
            objectName='DO1',
            objectType='binaryOutput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
    ), BinaryOutputObject(
            objectIdentifier=('binaryOutput',1),
            objectName='DO2',
            objectType='binaryOutput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
    ), BinaryOutputObject(
            objectIdentifier=('binaryOutput',2),
            objectName='SPA Reset',
            objectType='binaryOutput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
    )]

    multistate_input_objects = [MultiStateInputObject(
            objectIdentifier=('multiStateInput',0),
            objectName='Alarm Level',
            objectType='multiStateInput',
            presentValue=1,
            eventState='normal',
            outOfService=False,
            numberOfStates=3
    )]

    objects = analog_output_objets+analog_input_objects+analog_value_objects+binary_input_objects+binary_output_objects+multistate_input_objects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=381003, objectName="CDD_CO2_Detector_003", objectType=8, systemStatus='operational', vendorName='Greystone Energy Systems',
                                                             vendorIdentifier=381, modelName='CDD2A', firmwareRevision='1.4', applicationSoftwareVersion='1.0', description='Greystone CO2 Detector',protocolVersion=1, protocolRevision=10, maxapdulength=480,
                                                             segmentationSupported="noSegmentation", apduTimeout=3000, numberOfApduRetries=3, maxMaster=127, maxInfoFrames=1,
                                                             databaseRevision=0, objects=objects)

if __name__ == "__main__":
    print(run_application())