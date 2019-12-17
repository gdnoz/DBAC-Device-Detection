class DHCPSpoofing:

    @staticmethod
    def send_dhcp_discover(mud_url: str, mac: str, dhcp_fingerprint: list, dhcp_vendor: str):
        """
        To be used for testing only. Sends a spoofed DHCP Discover packet to the default ethernet interface of the localhost.
        :param mac: mac address of the spoofed device.
        :param dhcp_fingerprint: DHCP fingerprint of the spoofed device.
        :param dhcp_vendor: DHCP vendor of the spoofed device.
        :return:
        """

        from scapy.layers.dhcp import DHCP
        from scapy.layers.l2 import Ether
        from scapy.layers.dhcp import BOOTP
        from scapy.layers.inet import IP, UDP
        from scapy.volatile import RandInt
        from scapy.config import conf
        from scapy.sendrecv import sendp
        from scapy.arch import get_if_raw_hwaddr
        import socket

        _,localmacraw = get_if_raw_hwaddr(conf.iface)

        own_ip_address = socket.gethostbyname(socket.getfqdn())

        dhcp_discover_packet = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff', type=0x800)\
                        /IP(src='0.0.0.0', dst=own_ip_address)\
                        /UDP(dport=67, sport=68)\
                        /BOOTP(chaddr=localmacraw, ciaddr = '0.0.0.0',xid=RandInt(), flags = 1) \
                        /DHCP(options=[('message-type', 'discover'), ('param_req_list',) + tuple([x for x in dhcp_fingerprint]),('vendor_class_id', dhcp_vendor), (161, bytes(mud_url,encoding='utf8')), 'end'])

        print("Sending DHCP Discover packet to interface " + str(conf.iface) + "...")
        sendp(dhcp_discover_packet)

if __name__ == "__main__":
    #DHCPSpoofing.send_dhcp_discover("https://iotanalytics.unsw.edu.au/mud/samsungsmartcamMud.json", "00:A0:C9:14:C8",[1,33,3,6,15,28,51,58,59],"dhcpcd-5.2.10:Linux-3.8.13+:armv7l:Marvell Berlin SoC (Flattened Device Tree)")
    DHCPSpoofing.send_dhcp_discover("https://iotanalytics.unsw.edu.au/mud/hpprinterMud.json","00:00:00:00:7b:be",[1,33,3,6,12,15,28,51,58,59,119],"dhcpcd-5.2.10:Linux-3.8.13+")