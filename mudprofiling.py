class MUDProfiler:
    """
    Intercepts DHCP packets and performs profiling.
    Is used for profiling files by scraping the SystemInfo and MUD URLs to perform web scraping and classificationcreation of the device.
    Furthermore, DHCP fingerprinting also occurs.
    """

    def __init__(self, test=False):
        self.test = test

    def run(self):
        from dhcp.sniffer import DiscoveryPacketSniffer
        from dhcp.fingerprinting import FingerbankApi
        from mud.classification import MudClassification,MudClassificationResult
        from mud.utilities import MUDUtilities

        print("****************** Performing MUD Profiling ******************")

        print("****************** Sniffing for DHCP Packet ******************")

        sniff_result = DiscoveryPacketSniffer.sniff()

        print("****************** Packet obtained! **************************\n\n")
        print("******************** MUD Profiling Result ********************")

        mud_classification = MudClassification(0.6)

        if not self.test:
            classification_result = mud_classification.classify_mud_contents(MUDUtilities.get_mud_file(sniff_result.mud_url))
            print("Device type:             " + classification_result.predicted_class)
            print("Classification score:    " + str(classification_result.score))
        else:
            classification_result = mud_classification.classify_mud_file(sniff_result.mud_url)
            print("Device type:             " + classification_result.predicted_class)
            print("Classification score:    " + str(classification_result.score))

        fingerprint_result = FingerbankApi.interrogate(sniff_result.dhcp_fingerprint,sniff_result.dhcp_vendor,sniff_result.mac)

        print("Name:                    " + fingerprint_result.device_name)
        print("Fingerprint score:       " + str(fingerprint_result.score))

        print("Mud file ACLs:")
        print(MUDUtilities.extract_acls_from_mud_contents(MUDUtilities.get_mud_file(sniff_result.mud_url)))


if __name__ == "__main__":
    mud_profiler = MUDProfiler(test=False)
    mud_profiler.run()
