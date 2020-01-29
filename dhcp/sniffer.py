class DiscoveryPacketSniffer:
    """
    Utility class for sniffing for DHCP Discover Packets on the local ethernet interface.
    """

    FILTER_DHCP = "udp and src port 68 and dst port 67"

    @staticmethod
    def sniff():
        """
        Runs until a DHCP Discover packet is sniffed.
        :return: (dhcp_fingerprint, dhcp_vendor, mac)
        """
        from scapy.layers.dhcp import DHCP
        from scapy.layers.l2 import Ether
        from scapy.sendrecv import sniff
        from scapy.config import conf

        print("Listening for DHCP Discover packets on interface " + str(conf.iface) + "...")

        #Default interface is 'en0'
        sniffed_packet = sniff(iface=conf.iface,prn = lambda x: x.summary(),
                               filter=DiscoveryPacketSniffer.FILTER_DHCP,
                               lfilter=lambda p: DiscoveryPacketSniffer.is_discovery_packet(p),
                               count=1)

        dhcp_options_dictionary = dict([opt for opt in sniffed_packet[0][DHCP].options
                          if isinstance(opt, tuple) and len(opt) == 2])

        mud_url = dhcp_options_dictionary[161].decode("utf8")
        dhcp_fingerprint = dhcp_options_dictionary['param_req_list']
        dhcp_vendor = dhcp_options_dictionary.get('vendor_class_id').decode("utf8")
        mac = sniffed_packet[0][Ether].src

        return SniffResult(mud_url, dhcp_fingerprint, dhcp_vendor, mac)

    @staticmethod
    def is_discovery_packet(packet):
        from scapy.layers.dhcp import DHCP

        return DHCP in packet and packet[DHCP].options[0][1] == 1

class SniffResult:
    mud_url = ""
    dhcp_fingerprint = []
    dhcp_vendor = ""
    mac = ""
    device_id = 0

    def __init__(self, mud_url: str, dhcp_fingerprint: list, dhcp_vendor: str, mac: str, device_id: int = 0):
        SniffResult.mud_url = mud_url
        SniffResult.dhcp_fingerprint = dhcp_fingerprint
        SniffResult.dhcp_vendor = dhcp_vendor
        SniffResult.mac = mac
        SniffResult.device_id = device_id


if __name__ == "__main__":
    res = DiscoveryPacketSniffer.sniff()
    print(res)