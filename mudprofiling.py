class MUDProfiler:
    """
    Intercepts DHCP packets and performs profiling.
    Is used for profiling files by web_scraping the SystemInfo and MUD URLs to perform web web_scraping and device_classification of the device.
    Furthermore, DHCP fingerprinting also occurs.
    """

    sniff_result = None

    def __init__(self, sniff_result=None):
        self.sniff_result = sniff_result

    def run(self):
        from dhcp.sniffer import DiscoveryPacketSniffer
        from dhcp.fingerprinting import FingerbankApi
        from mud.classification import MudClassification,MudClassificationResult
        from mud.utilities import MUDUtilities

        if self.sniff_result == None:
            print("****************** Performing MUD Profiling ******************")

            print("****************** Sniffing for DHCP Packet ******************")

            self.sniff_result = DiscoveryPacketSniffer.sniff()

            print("*********************** Packet obtained! *********************\n\n")

        mud_classification = MudClassification(0.2**2, 0.2)

        mud_file_from_web = MUDUtilities.get_mud_file(self.sniff_result.mud_url)

        print("******************** MUD profiling result ********************")

        classification_result = mud_classification.classify_mud_contents(mud_file_from_web)
        print("Device type:             " + classification_result.predicted_class)
        print("Classification score:    " + str(classification_result.score))

        if self.sniff_result.device_id > 0:
            fingerprint_result = FingerbankApi.get_device_from_id(self.sniff_result.device_id)
            deviceid = (fingerprint_result.device_manufacturer + '.' + fingerprint_result.device_name).replace(" ", "")
        else:
            #fingerprint_result = FingerbankApi.interrogate(self.sniff_result.dhcp_fingerprint,self.sniff_result.dhcp_vendor,self.sniff_result.mac)
            deviceid = ("UNKNOWN.UNKNOWN")

        print("Name:                    " + deviceid)
        #print("Fingerprint score:       " + str(fingerprint_result.score))

        acl_list = MUDUtilities.get_acl_list_json(MUDUtilities.extract_acls_from_mud_contents(mud_file_from_web))
        print("Mud file ACLs:")

        acl_profile = mud_classification.generate_acl_profile(deviceid, acl_list)
        sxc_contract = MUDUtilities.generate_contract_from_acl_profile(acl_profile)
        print(sxc_contract)

        contacts_all = set.union(acl_profile.contacts_in, acl_profile.contacts_out)
        print('Contact domains:')
        for dom in contacts_all:
            print('\t'+dom)

        print("******************** MUD profiling completed *****************")

if __name__ == "__main__":
    mud_profiler = MUDProfiler()
    mud_profiler.run()