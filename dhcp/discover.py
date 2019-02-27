class DHCPSpoofing:

    @staticmethod
    def send_dhcp_discover(mac: str, dhcp_fingerprint: list, dhcp_vendor: str):
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
        from scapy.arch import get_if_hwaddr

        localmac = get_if_hwaddr(conf.iface)
        localmacraw = localmac.replace(':', '').decode('hex')


        dhcp_discover = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff')\
                        /IP(src='0.0.0.0', dst='255.255.255.255')\
                        /UDP(dport=67, sport=68)\
                        /BOOTP(chaddr=localmacraw,xid=RandInt())\
                        /DHCP(options=[('message-type', 'discover'),('param_req_list',)+tuple([chr(x) for x in dhcp_fingerprint]),('vendor_class_id',dhcp_vendor), 'end'])

        #https://programtalk.com/python-examples/scapy.all.DHCPRevOptions/

if __name__ == "__main__":
    print(('param_req_list',) + tuple([chr(x) for x in [1,2,3,6,7]]))