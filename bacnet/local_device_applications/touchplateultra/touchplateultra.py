'''
Based on: https://touchplate.com/wp-content/uploads/2013/11/Ultra-BACnet-Manual-Rev2.0a-Digital.pdf

Simulates and queries device based on the above data sheet.
'''

def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''
    from bacpypes.object import AnalogInputObject,AnalogOutputObject,AnalogValueObject,BinaryInputObject,BinaryOutputObject,MultiStateInputObject
    from bacnet.local_device_applications import SimulateAndQueryDeviceApplication

    binary_input_objects = \
        [BinaryInputObject(
            objectIdentifier=('binaryInput',1),
            objectType='binaryInput',
            objectName='Momentary01',
            presentValue=0,
            deviceType='Momentary Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',2),
            objectType='binaryInput',
            objectName='Momentary02',
            presentValue=0,
            deviceType='Momentary Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',3),
            objectType='binaryInput',
            objectName='Momentary03',
            presentValue=0,
            deviceType='Momentary Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',4),
            objectType='binaryInput',
            objectName='Momentary04',
            presentValue=0,
            deviceType='Momentary Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',5),
            objectType='binaryInput',
            objectName='Momentary05',
            presentValue=0,
            deviceType='Momentary Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',6),
            objectType='binaryInput',
            objectName='Momentary06',
            presentValue=0,
            deviceType='Momentary Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',101),
            objectType='binaryInput',
            objectName='Maintained01',
            presentValue=0,
            deviceType='Maintain Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',102),
            objectType='binaryInput',
            objectName='Maintained02',
            presentValue=0,
            deviceType='Maintain Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',103),
            objectType='binaryInput',
            objectName='Maintained03',
            presentValue=0,
            deviceType='Maintain Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',104),
            objectType='binaryInput',
            objectName='Maintained04',
            presentValue=0,
            deviceType='Maintain Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',105),
            objectType='binaryInput',
            objectName='Maintained05',
            presentValue=0,
            deviceType='MomeMaintainntary Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        ), BinaryInputObject(
            objectIdentifier=('binaryInput',106),
            objectType='binaryInput',
            objectName='Maintained06',
            presentValue=0,
            deviceType='Maintain Contact',
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            polarity='normal',
            activeText='on',
            inactiveText='off'
        )]

    analog_value_objects = [AnalogValueObject(
        objectIdentifier=('analogValue', 1),
        objectType='analogValue',
        objectName='Pilot01',
        presentValue=0x0110101,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 2),
        objectType='analogValue',
        objectName='Pilot02',
        presentValue=0x0101101,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 3),
        objectType='analogValue',
        objectName='Pilot03',
        presentValue=0x111001,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 4),
        objectType='analogValue',
        objectName='Pilot04',
        presentValue=0x0110110,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 5),
        objectType='analogValue',
        objectName='Pilot05',
        presentValue=0x0000101,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 6),
        objectType='analogValue',
        objectName='Pilot06',
        presentValue=0x0000001,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 100),
        objectType='analogValue',
        objectName='Device Options',
        presentValue=0,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 1001),
        objectType='analogValue',
        objectName='Input Change Buffer',
        presentValue=0,
        eventState='normal',
        outOfService=False,
    ), AnalogValueObject(
        objectIdentifier=('analogValue', 1003),
        objectType='analogValue',
        objectName='Device Instance',
        presentValue=0,
        eventState='normal',
        outOfService=False,
    )]

    objects = analog_value_objects+binary_input_objects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=68501, objectName="BAC10142XXXXXXXX", objectType=8, systemStatus='operational', vendorName='Touch-Plate Lighting Controls',
                                                             vendorIdentifier=68, modelName='Ultra BACnet Smart Control Station', firmwareRevision='2.48', applicationSoftwareVersion='1.5h',
                                                             protocolVersion=1, protocolRevision=7, protocolObjectTypesSupported=['analogValue','binaryInput','binaryOutput','device'],maxapdulength=480,
                                                             segmentationSupported="noSegmentation", apduTimeout=3000, numberOfApduRetries=0, maxMaster=127, databaseRevision=1, objects=objects)

if __name__ == "__main__":
    print(run_application())