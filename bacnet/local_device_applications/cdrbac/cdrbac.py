'''
Based on: http://ctsteknik.dk/upload_dir/shop/SN1.405-CDR-BAC.pdf
'''

def main():
    import bacnet.LocalDeviceApplication as LocalDeviceApplication

    from bacpypes.object import AnalogInputObject
    import bacpypes.basetypes

    analog_input_object = AnalogInputObject(
        objectName='Temperature Sensor',
        objectIdentifier=('analogInput', 0),
        objectType='analogInput',
        presentValue=21,
        statusFlags=bacpypes.basetypes.StatusFlags.bitNames['inAlarm'],
        eventState=bacpypes.basetypes.EventState.enumerations['normal'],
        outOfService=False,
        units='degreesCelsius'
    )

    objects = [analog_input_object]


    LocalDeviceApplication.run_application(objectname="cdrbac", objectidentifier=599, maxapdulength= 1024,
                                           segmentationsupported="segmentedBoth", vendoridentifier=15, objects=objects)

if __name__ == "__main__":
    main()