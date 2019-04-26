#!/usr/bin/env python

"""
Modified version of https://github.com/JoelBender/bacpypes/blob/master/samples/Tutorial/SampleConsoleCmd.py
under MIT license.

Base application for spoofing a bacnet device on the local network.
To use the ini arguments of the starting script must be passed and all objects
that are going to be associated with the spoofed device must be passed.
"""

from bacpypes.debugging import bacpypes_debugging, ModuleLogger

from bacpypes.core import run, enable_sleeping

from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject
from bacpypes.object import Object

from typing import List

_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
class DebugApplication(BIPSimpleApplication):
    def __init__(self, device, address):
        if _debug: DebugApplication._debug("__init__ %r %r", device, address)
        BIPSimpleApplication.__init__(self, device, address)

    def request(self, apdu):
        if _debug: DebugApplication._debug("request %r", apdu)
        BIPSimpleApplication.request(self, apdu)

    def indication(self, apdu):
        if _debug: DebugApplication._debug("indication %r", apdu)
        BIPSimpleApplication.indication(self, apdu)

    def response(self, apdu):
        if _debug: DebugApplication._debug("response %r", apdu)
        BIPSimpleApplication.response(self, apdu)

    def confirmation(self, apdu):
        if _debug: DebugApplication._debug("confirmation %r", apdu)
        BIPSimpleApplication.confirmation(self, apdu)

def run_application(ini, objects: List[Object]):
    '''
    Running the base application for spoofing bacnet devices on the local network.
    :param ini: Ini parameters
    :param objects: Objects to be attached to the device
    :return:
    '''
    this_device = LocalDeviceObject(
        objectName=ini.objectname,
        objectIdentifier=int(ini.objectidentifier),
        maxApduLengthAccepted=int(ini.maxapdulengthaccepted),
        segmentationSupported=ini.segmentationsupported,
        vendorIdentifier=int(ini.vendoridentifier)
    )

    this_application = DebugApplication(this_device, ini.address)

    for object in objects:
        this_application.add_object(object)

    enable_sleeping()

    run()