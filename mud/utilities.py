

class MUDUtilities:
    """
    A utility class for scraping html from a url and also cleaning the text.
    """
    @staticmethod
    def extract_acls_from_mud(filename: str) -> str:
        """
        Extracts the policies and ACLs from a specified mudfile.
        :param filename: Filename of mudfile.
        :return: Pretty string representation.
        """
        import os,json,constants

        policy_acl_dict = dict()

        with open(os.path.join(constants.MUDFILES_DIR,filename)) as f:
            mud_file_contents = json.load(f)

            if 'from-device-policy' in mud_file_contents['ietf-mud:mud']:
                policy_acl_dict['from-device-policy'] = mud_file_contents['ietf-mud:mud']['from-device-policy']

            if 'to-device-policy' in mud_file_contents['ietf-mud:mud']:
                policy_acl_dict['to-device-policy'] = mud_file_contents['ietf-mud:mud']['to-device-policy']

            if 'ietf-access-control-list:access-lists' in mud_file_contents and 'acl' in mud_file_contents['ietf-access-control-list:access-lists']:
                policy_acl_dict['acls'] = mud_file_contents['ietf-access-control-list:access-lists']['acl']

        return json.dumps(policy_acl_dict, indent=4)

    @staticmethod
    def get_all_urls_from_mud(filename: str) -> set:
        """
        Retrieves all URLs contained in the ACLs of the given mud file.
        :param filename: File name of the mud file.
        :return: List of URLs.
        """
        import os,json,constants

        with open(os.path.join(constants.MUDFILES_DIR, filename)) as f:
            mud_contents = json.load(f)
            urls = set()

            for k in mud_contents["ietf-access-control-list:access-lists"]["acl"]:

                for ace in k["aces"]["ace"]:
                    try:
                        urls.add(ace["matches"]["ipv4"]["ietf-acldns:dst-dnsname"])
                    except KeyError:
                        continue

        return urls

    @staticmethod
    def get_systeminfo_from_mud_file(filename: str) -> str:
        import os,json,constants

        with open(os.path.join(constants.MUDFILES_DIR, filename)) as f:
            mud_contents = json.load(f)
            systeminfo = mud_contents['ietf-mud:mud']['systeminfo']

        return systeminfo


    @staticmethod
    def get_mud_files():
        """
        Retrieves the mud files, given by the URLs in the 'mud_file_urls.csv* file.
        """
        import ssl,os,constants
        from scraping.utilities import WebScrapingUtilities

        ssl._create_default_https_context = ssl._create_unverified_context

        if not os.path.exists(constants.MUDFILES_DIR):
            os.mkdir(constants.MUDFILES_DIR)

        with open(constants.MUD_FILE_URLS_FILE_PATH,"r") as f:
            for line in f.readlines():
                items = line.split(",")
                url = items[0]
                device = items[1].rstrip()

                WebScrapingUtilities.get_content_from_url_and_save(url, constants.MUDFILES_DIR, device + ".json")