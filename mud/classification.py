class MudClassificationResult:
    predicted_class = ""
    score = 0.0

    def __init__(self, predicted_class: str, score: float):
        self.predicted_class = predicted_class
        self.score = score

class MudAclProfile:
    provides_lan = set([])
    provides_net = set([])
    uses_lan = set([])
    uses_net = set([])

    def __init__(self, provides_lan: set,
                       provides_net: set,
                       uses_lan: set,
                       uses_net: set):
        self.provides_lan = provides_lan
        self.provides_net = provides_net
        self.uses_lan = uses_lan
        self.uses_net = uses_net

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

    def generate_acl_profile(acl_list: dict) -> MudAclProfile:
        """
        Generates lists of services provided and used over the internet and LAN
        from MUD ACLs
        """
        from mud.utilities import MUDUtilities


        provides_lan = set([])
        provides_net = set([])
        uses_lan = set([])
        uses_net = set([])
        
        for a in acl_list:
            print(a['name'])

            outbound = a['name'].startswith('from')
            port_prefix = 'destination-' if outbound else 'source-'
            dns_prefix = 'ietf-acldns:dst-' if outbound else 'ietf-acldns:src-'

            acl = MUDUtilities.get_acl_from_acl_list_item(a)

            for ace in acl:
                service_port = -1
                dname = ''
                print('\t ace: ' + ace['name'])
                for rule in ace['matches']:
                    # TODO: Is this even important?
                    # try:
                    #     service['protocol'] = MUDUtilities.get_protocol_name_from_num(ace['matches'][rule]['protocol'])
                    # except KeyError:
                    #     pass
                    try:
                        dname = ace['matches'][rule][dns_prefix + 'dnsname']
                    except KeyError:
                        pass
                    try:
                        # TODO: Different operators? (not just eq)
                        service_port = int(ace['matches'][rule][port_prefix + 'port']['port'])
                    except KeyError:
                        pass
                    
                    print('\t\t matches: ' + str(rule))
                    try:
                        print('\t\t\t rule: ' + str(ace['matches'][rule]))
                    except KeyError:
                        pass

                local = dname == ''

                if   service_port >= 0 and outbound and local:          uses_lan.add(service_port)
                elif service_port >= 0 and outbound and not local:      uses_net.add(service_port)
                elif service_port >= 0 and not outbound and local:      provides_lan.add(service_port)
                elif service_port >= 0 and not outbound and not local:  provides_net.add(service_port)


        return MudAclProfile(provides_lan, provides_net, uses_lan, uses_net)
