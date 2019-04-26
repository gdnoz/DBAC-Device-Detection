'''
Based on: http://ctsteknik.dk/upload_dir/shop/SN1.405-CDR-BAC.pdf
'''

def main():
    import bacnet.LocalDeviceApplication as LocalDeviceApplication

    from bacpypes.object import Object, ObjectIdentifierProperty, AnalogInputObject, ObjectIdentifier
    import bacpypes.basetypes

    from bacpypes.consolelogging import ConfigArgumentParser

    args = ConfigArgumentParser(description=__doc__).parse_args()

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

    LocalDeviceApplication.run_application(args.ini, objects)

if __name__ == "__main__":
    main()