from mudprofiling import MUDProfiler
from dhcp.sniffer import SniffResult

def get_sniff_result(device: str) -> SniffResult:
    mud_url = 'https://iotanalytics.unsw.edu.au/mud/' + device + '.json'
    fingerprint = [1,33,3,6,12,15,28,51,58,59,119]
    vendor_str = "dhcpcd-5.2.10:Linux-3.8.13+"
    mac = "00:00:00:00:7b:be"

    return SniffResult(mud_url, fingerprint, vendor_str, mac)

devices = [
    'amazonEchoMud',
    'augustdoorbellcamMud',
    'awairAirQualityMud',
    'belkincameraMud',
    'blipcareBPmeterMud',
    'canaryCameraMud',
    'chromecastUltraMud',
    'dropcamMud',
    'hellobarbieMud',
    'hpprinterMud',
    'HueBulbMud',
    'ihomepowerplugMud',
    'lifxbulbMud',
    'nestsmokesensorMud',
    'NetatmoCameraMud',
    'NetatmoWeatherStationMud',
    'pixstarphotoframeMud',
    'ringdoorbellMud',
    'samsungsmartcamMud',
    'SmartThingsMud',
    'tplinkcameraMud',
    'tplinkplugMud',
    'tribyspeakerMud',
    'wemomotionMud',
    'wemoswitchMud',
    'withingsbabymonitorMud',
    'withingscardioMud',
    'withingssleepsensorMud'
]

for device in devices:
    print('testing', device)
    mud_profiler = MUDProfiler(get_sniff_result(device))
    mud_profiler.run()