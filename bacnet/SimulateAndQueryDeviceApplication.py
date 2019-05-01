import threading, asyncio
from typing import List

from bacpypes.object import Object
from bacnet import LocalDeviceApplication
import bacnet.ReadAllObjectPropertiesApp as raop

'''
Class for simulating a BACnet device and then querying it of it's objects.
'''

def run_application(objectname: str, objectidentifier: int, maxapdulength: int, segmentationsupported: str,
                    vendoridentifier: int, objects: List[Object]) -> str:

    thread = threading.Thread(target=LocalDeviceApplication.run_application, args=(objectname, objectidentifier, maxapdulength,
                                                                                   segmentationsupported, vendoridentifier, objects))
    thread.start()
    raop.run_application()

    asyncio.wait_for(raop.query_output, timeout=10)
    return raop.query_output.result()
