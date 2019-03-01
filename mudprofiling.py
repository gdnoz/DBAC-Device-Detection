class MUDProfiler:
    """
    Intercepts DHCP packets and performs profiling.
    Is used for profiling files by scraping the SystemInfo and MUD URLs to perform web scraping and classificationcreation of the device.
    Furthermore, DHCP fingerprinting also occurs.
    """

    def __init__(self, use_mud_manager: bool):
        self.use_mud_manager = use_mud_manager

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

        if self.use_mud_manager:
            #Implement mud manager usage.
            print("*************** MUD Manager not implemented! ***********************")
            return
        else:
            classification_result = mud_classification.classify_mud(sniff_result.mud_url)
            print("Device type:             " + classification_result.predicted_class)
            print("Classification score:    " + str(classification_result.score))

        fingerprint_result = FingerbankApi.interrogate(sniff_result.dhcp_fingerprint,sniff_result.dhcp_vendor,sniff_result.mac)

        print("Name:                    " + fingerprint_result.device_name)
        print("Fingerprint score:       " + str(fingerprint_result.score))

        print("Mud file ACLs:")
        print(MUDUtilities.extract_acls_from_mud(sniff_result.mud_url))


if __name__ == "__main__":
    mud_profiler = MUDProfiler(use_mud_manager=False)
    mud_profiler.run()
