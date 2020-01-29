from mudprofiling import MUDProfiler
from dhcp.sniffer import SniffResult

def get_sniff_result(device: dict) -> SniffResult:
    mud_url = 'https://iotanalytics.unsw.edu.au/mud/' + device['name'] + '.json'
    fingerprint = []
    vendor_str = ""
    mac = ""

    return SniffResult(mud_url, fingerprint, vendor_str, mac, device['id'])

devices = [
    {'name':'amazonEchoMud',            'id':15666},#
    {'name':'augustdoorbellcamMud',     'id':49529},#
    {'name':'awairAirQualityMud',       'id':50378},#
    {'name':'belkincameraMud',          'id':39881},#
    {'name':'blipcareBPmeterMud',       'id':25485},#?
    {'name':'canaryCameraMud',          'id':36963},#?
    {'name':'chromecastUltraMud',       'id':49244},#
    {'name':'dropcamMud',               'id':33475},#
    {'name':'hellobarbieMud',           'id':61588},#?
    {'name':'hpprinterMud',             'id':157},#
    {'name':'HueBulbMud',               'id':50151},#
    {'name':'ihomepowerplugMud',        'id':49667},#
    {'name':'lifxbulbMud',              'id':12759},#
    {'name':'nestsmokesensorMud',       'id':33476},#
    {'name':'NetatmoCameraMud',         'id':73007},#
    {'name':'NetatmoWeatherStationMud', 'id':50048},#
    {'name':'pixstarphotoframeMud',     'id':49218},#
    {'name':'ringdoorbellMud',          'id':51268},#
    {'name':'samsungsmartcamMud',       'id':8109},#
    {'name':'SmartThingsMud',           'id':15909},#
    {'name':'tplinkcameraMud',          'id':15673},#
    {'name':'tplinkplugMud',            'id':43324},#
    {'name':'tribyspeakerMud',          'id':49362},#
    {'name':'wemomotionMud',            'id':33694},#
    {'name':'wemoswitchMud',            'id':33876},
    {'name':'withingsbabymonitorMud',   'id':49153},#
    {'name':'withingscardioMud',        'id':33908},#
    {'name':'withingssleepsensorMud',   'id':42476}#
]

for device in devices:
    print('testing', device)
    mud_profiler = MUDProfiler(get_sniff_result(device))
    mud_profiler.run()