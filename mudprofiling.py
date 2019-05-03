class MUDProfiler:
    """
    Intercepts DHCP packets and performs profiling.
    Is used for profiling files by web_scraping the SystemInfo and MUD URLs to perform web web_scraping and device_classification of the device.
    Furthermore, DHCP fingerprinting also occurs.
    """

    def __init__(self, local_mud_file=False):
        self.local_mud_file = local_mud_file

    def run(self):
        from dhcp.sniffer import DiscoveryPacketSniffer
        from dhcp.fingerprinting import FingerbankApi
        from mud.classification import MudClassification,MudClassificationResult
        from mud.utilities import MUDUtilities

        print("****************** Performing MUD Profiling ******************")

        print("****************** Sniffing for DHCP Packet ******************")

        sniff_result = DiscoveryPacketSniffer.sniff()

        print("*********************** Packet obtained! *********************\n\n")

        mud_classification = MudClassification(0.2, 0.1)

        mud_file_from_web = MUDUtilities.get_mud_file(sniff_result.mud_url)

        print("******************** MUD profiling result ********************")

        if not self.local_mud_file:
            classification_result = mud_classification.classify_mud_contents(mud_file_from_web)
            print("Device type:             " + classification_result.predicted_class)
            print("Classification score:    " + str(classification_result.score))
        else: #In this case, the url is just a file path to a mud file on the machine.
            classification_result = mud_classification.classify_mud_file(sniff_result.mud_url)
            print("Device type:             " + classification_result.predicted_class)
            print("Classification score:    " + str(classification_result.score))

        fingerprint_result = FingerbankApi.interrogate(sniff_result.dhcp_fingerprint,sniff_result.dhcp_vendor,sniff_result.mac)

        print("Name:                    " + fingerprint_result.device_name)
        print("Fingerprint score:       " + str(fingerprint_result.score))

        print("Mud file ACLs:")
        print(MUDUtilities.extract_acls_from_mud_contents(mud_file_from_web))

        print("******************** MUD profiling completed *****************")

if __name__ == "__main__":
    mud_profiler = MUDProfiler(local_mud_file=False)
    mud_profiler.run()