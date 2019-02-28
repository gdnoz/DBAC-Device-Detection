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
        from mud.classification import MudClassification,MudClassificationResult
        from dhcp.fingerprinting import FingerbankApi

        print("****************** Performing MUD Profiling ******************")

        print("****************** Sniffing for DHCP Packet ******************")

        sniff_result = DiscoveryPacketSniffer.sniff()

        print("****************** Packet obtained! **************************")
        print("******************** MUD Profiling Result ********************")

        mud_classification = MudClassification(0.6)

        if self.use_mud_manager:
            #Implement mud manager usage.
            print("*************** MUD Manager not implemented! ***********************")
            return
        else:
            classification_result = mud_classification.classify_mud(sniff_result.mud_url)
            print("Device type:             " + classification_result.predicted_class)
            print("Classification score:    " + classification_result.score)

        fingerprint_result = FingerbankApi.interrogate(sniff_result.dhcp_fingerprint,sniff_result.dhcp_vendor,sniff_result.mac)

        print("Name:                    " + fingerprint_result.device_name)
        print("Fingerprint score:       " + fingerprint_result.score)

if __name__ == "__main__":
    mud_profiler = MUDProfiler(use_mud_manager=False)
    mud_profiler.run()
