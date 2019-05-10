'''
Based on: http://www.syxthsense.com/product/product_pdf/CT2.141-SRC-100-BAC.pdf

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

    analog_input_objects = [AnalogInputObject(
        objectName='Built-In Temperature Sensor',
        objectIdentifier=('analogInput', 1),
        objectType='analogInput',
        presentValue=21,
        eventState='normal',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectName='External Temperature Sensor',
        objectIdentifier=('analogInput', 2),
        objectType='analogInput',
        presentValue=87,
        eventState='normal',
        outOfService=False,
        units='degreesCelsius'
    ), AnalogInputObject(
        objectName='Calculated Setpoint',
        objectIdentifier=('analogInput', 3),
        objectType='analogInput',
        presentValue=87,
        eventState='normal',
        outOfService=False,
        units='degreesCelsius'
    )]

    analog_output_objets = [AnalogOutputObject(
            objectIdentifier=('analogOutput',1),
            objectName='Y1',
            objectType='analogOutput',
            presentValue=12,
            eventState='normal',
            outOfService=False,
            units='percent'
    ), AnalogOutputObject(
            objectIdentifier=('analogOutput',2),
            objectName='Y2',
            objectType='analogOutput',
            presentValue=88,
            eventState='normal',
            outOfService=False,
            units='percent'
    ), AnalogOutputObject(
            objectIdentifier=('analogOutput',3),
            objectName='Y3',
            objectType='analogOutput',
            presentValue=62,
            eventState='normal',
            outOfService=False,
            units='percent'
    ), AnalogOutputObject(
            objectIdentifier=('analogOutput',4),
            objectName='Thermic1_Position',
            objectType='analogOutput',
            presentValue=10,
            eventState='normal',
            outOfService=False,
            units='percent'
    ), AnalogOutputObject(
            objectIdentifier=('analogOutput',5),
            objectName='Thermic2_Position',
            objectType='analogOutput',
            presentValue=97,
            eventState='normal',
            outOfService=False,
            units='percent'
    ), AnalogOutputObject(
            objectIdentifier=('analogOutput',6),
            objectName='ThreePoint_Position',
            objectType='analogOutput',
            presentValue=62,
            eventState='normal',
            outOfService=False,
            units='percent'
    )]

    analog_value_objects = [AnalogValueObject(
            objectIdentifier=('analogValue',0),
            objectName='Temperature Setpoint',
            objectType='analogValue',
            presentValue=18,
            eventState='normal',
            outOfService=False,
            units='degreesCelsius',
            relinquishDefault=20
    ), AnalogValueObject(
            objectIdentifier=('analogValue',1),
            objectName='LCD Brightness',
            objectType='analogValue',
            presentValue=3.5,
            eventState='normal',
            outOfService=False,
            units='percent',
            relinquishDefault=50
    )]

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
            objectName='Night_Mode_Override',
            objectType='binaryOutput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
    ), BinaryOutputObject(
            objectIdentifier=('binaryOutput',3),
            objectName='Summer_Winter_Changeover',
            objectType='binaryOutput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
    ), BinaryOutputObject(
            objectIdentifier=('binaryOutput',4),
            objectName='Cooling_Disable',
            objectType='binaryOutput',
            presentValue=0,
            eventState='normal',
            outOfService=False,
            polarity='normal',
            relinquishDefault=0,
            activeText='on',
            inactiveText='off'
    )]

    objects = analog_output_objets + analog_input_objects + analog_value_objects + binary_input_objects + binary_output_objects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=651000, objectName="SRC100_001",
                                                             objectType='device', systemStatus='operational',
                                                             vendorName='SyxthSense',
                                                             vendorIdentifier=651, modelName='URD',
                                                             protocolVersion=1, protocolRevision=10,
                                                             maxapdulength=480, segmentationSupported="noSegmentation",
                                                             apduTimeout=3000, numberOfApduRetries=3,
                                                             maxMaster=127, maxInfoFrames=1, databaseRevision=0,
                                                             objects=objects)

if __name__ == "__main__":
    print(run_application())