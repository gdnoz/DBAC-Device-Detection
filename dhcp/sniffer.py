"""
https://github.com/juga0/dhcpcfp example of dhcp sniffing
FILTER_DHCP_MAC = "udp and src port 68 and dst port 67" \
                      " and ether src {}"
"""

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

        #Default interface is 'en0'
        sniffed_packet = sniff(iface=conf.iface,
                            filter=DiscoveryPacketSniffer.FILTER_DHCP,
                            lfilter=lambda p: DiscoveryPacketSniffer.is_discovery_packet(p),
                            monitor=True)

        dhcp_options_dictionary = dict([opt for opt in sniffed_packet[DHCP].options
                          if isinstance(opt, tuple) and len(opt) == 2])

        dhcp_fingerprint = [ord(option) for option in dhcp_options_dictionary['param_req_list']]
        dhcp_vendor = dhcp_options_dictionary.get('vendor_class_id')
        mac = sniffed_packet[Ether].src

        return (dhcp_fingerprint, dhcp_vendor, mac)

    @staticmethod
    def is_discovery_packet(packet):
        from scapy.layers.dhcp import DHCP

        """
        DHCP Message Types:
        
           Value   Message Type
           -----   ------------
             1     DHCPDISCOVER
             2     DHCPOFFER
             3     DHCPREQUEST
             4     DHCPDECLINE
             5     DHCPACK
             6     DHCPNAK
             7     DHCPRELEASE
             8     DHCPINFORM
             
        Source: https://tools.ietf.org/html/rfc2132, Section 9.6
        """

        return DHCP in packet and packet[DHCP].options[0][1] == 1


if __name__ == "__main__":
    DiscoveryPacketSniffer.sniff()