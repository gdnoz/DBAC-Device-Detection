import asyncio
import threading
from typing import List

from bacpypes.object import Object

from bacnet.local_device_applications import LocalDeviceApplication, ReadAllObjectPropertiesApp

'''
Class for simulating a BACnet device and then querying it of it's objects.
'''

def run_application(**kwargs) -> str:
    '''
    Simulates the device given the specified arguments and returns the query of it's objects.
    :param objectname:
    :param objectidentifier:
    :param maxapdulength:
    :param segmentationsupported:
    :param vendoridentifier:
    :param objects:
    :return:
    '''

    thread = threading.Thread(target=LocalDeviceApplication.run_application, kwargs=kwargs)
    thread.start()

    #Give object identifier of the device object that will be queried.
    ReadAllObjectPropertiesApp.run_application(kwargs["objectIdentifier"])

    asyncio.get_event_loop().run_until_complete(asyncio.wait_for(ReadAllObjectPropertiesApp.query_output, timeout=30))

    return ReadAllObjectPropertiesApp.query_output.result()
