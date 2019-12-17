class MudClassificationResult:
    predicted_class = ""
    score = 0.0

    def __init__(self, predicted_class: str, score: float):
        self.predicted_class = predicted_class
        self.score = score

class MudAclProfile:
    device = ''
    provides_lan = set([])
    provides_net = set([])
    uses_lan = set([])
    uses_net = set([])
    contacts_out = set([])
    contacts_in = set([])

    def __init__(self, device: str,
                       provides_lan: set,
                       provides_net: set,
                       uses_lan: set,
                       uses_net: set,
                       contacts_out: set,
                       contacts_in: set):
        self.device = device
        self.provides_lan = provides_lan
        self.provides_net = provides_net
        self.uses_lan = uses_lan
        self.uses_net = uses_net
        self.contacts_out = contacts_out
        self.contacts_in = contacts_in

class MudClassification:
    """
    Given a mud file as input, the file will be used to classify the type of the device.
    """

    def __init__(self, classification_threshold: float, snippet_threshold: float):
        from device_classification.text_classification import DeviceClassifier
        self.threshold = classification_threshold
        self.snippet_threshold = snippet_threshold
        self.classifier = DeviceClassifier(threshold=classification_threshold)

    def classify_mud_file(self, filename: str) -> MudClassificationResult:
        """
        Classifies device type that the specified mud file describes.
        :param filename: Filename of the mud file.
        :return: Classified class and score
        """

        print("Classifying " + filename + "...")
        from mud.utilities import MUDUtilities

        return self.classify_mud_contents(MUDUtilities.get_mud_file_contents(filename))

    def classify_mud_contents(self, mud_file_contents: str) -> MudClassificationResult:
        '''
        Classifies device based on the contents of a mud file.
        :param mud_file_contents:
        :return: Classified class and score
        '''

        from mud.utilities import MUDUtilities
        from web_scraping.bing import BingSearchAPI
        from web_scraping.google import GoogleCustomSearchAPI

        systeminfo = MUDUtilities.get_systeminfo_from_mud_file(mud_file_contents)

        snippets = BingSearchAPI.first_ten_snippets(systeminfo)+GoogleCustomSearchAPI.search_text(systeminfo)

        classification_result = self.classifier.predict_snippets(snippets, self.snippet_threshold)

        return MudClassificationResult(classification_result.predicted_class, classification_result.prediction_probability)

    def generate_acl_profile(self, device: str, acl_list: dict) -> MudAclProfile:
        """
        Generates lists of services provided and used over the internet and LAN
        from MUD ACLs
        """
        from mud.utilities import MUDUtilities

        provides_lan = set([])
        provides_net = set([])
        uses_lan = set([])
        uses_net = set([])
        contacts_out = set([])
        contacts_in = set([])

        for a in acl_list:
            outbound = a['name'].startswith('from')
            port_prefix = 'destination-' if outbound else 'source-'
            dns_prefix = 'ietf-acldns:dst-' if outbound else 'ietf-acldns:src-'

            acl = MUDUtilities.get_acl_from_acl_list_item(a)

            for ace in acl:
                service = ''
                dname = ''
                
                for rule in ace['matches']:
                    try:
                        dname = ace['matches'][rule][dns_prefix + 'dnsname']
                    except KeyError:
                        pass
                    try:
                        # TODO: Different operators? (not just eq)
                        service = str(ace['matches'][rule][port_prefix + 'port']['port'])
                    except KeyError:
                        pass

                local = dname == ''

                # if dname != '':
                #     service = dname+':'+service

                if outbound:
                    contacts_out.add(dname)
                else:
                    contacts_in.add(dname)

                if   service != '' and outbound and local:          uses_lan.add(service)
                elif service != '' and outbound and not local:      uses_net.add(service)
                elif service != '' and not outbound and local:      provides_lan.add(service)
                elif service != '' and not outbound and not local:  provides_net.add(service)

        return MudAclProfile(device, provides_lan, provides_net, uses_lan, uses_net, contacts_out, contacts_in)
