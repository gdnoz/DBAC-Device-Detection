class MUDUtilities:
    """
    A utility class for web_scraping html from a url and also cleaning the text.
    """

    @staticmethod
    def extract_acls_from_mud(filename: str) -> str:
        """
        Extracts the policies and ACLs from a specified mudfile.
        :param filename: Filename of mudfile.
        :return: Pretty string representation.
        """
        import os, json, constants

        policy_acl_dict = dict()

        with open(os.path.join(constants.MUDFILES_DIR, filename)) as f:
            mud_file_contents = json.load(f)

            if 'from-device-policy' in mud_file_contents['ietf-mud:mud']:
                policy_acl_dict['from-device-policy'] = mud_file_contents['ietf-mud:mud']['from-device-policy']

            if 'to-device-policy' in mud_file_contents['ietf-mud:mud']:
                policy_acl_dict['to-device-policy'] = mud_file_contents['ietf-mud:mud']['to-device-policy']

            if 'ietf-access-control-list:access-lists' in mud_file_contents and 'acl' in mud_file_contents[
                'ietf-access-control-list:access-lists']:
                policy_acl_dict['acls'] = mud_file_contents['ietf-access-control-list:access-lists']['acl']

        return json.dumps(policy_acl_dict, indent=4)

    @staticmethod
    def extract_acls_from_mud_contents(mud_file_contents: str) -> str:
        import json

        policy_acl_dict = dict()

        mud_file_contents_dict = json.loads(mud_file_contents)

        if 'from-device-policy' in mud_file_contents_dict['ietf-mud:mud']:
            policy_acl_dict['from-device-policy'] = mud_file_contents_dict['ietf-mud:mud']['from-device-policy']

        if 'to-device-policy' in mud_file_contents_dict['ietf-mud:mud']:
            policy_acl_dict['to-device-policy'] = mud_file_contents_dict['ietf-mud:mud']['to-device-policy']

        if 'ietf-access-control-list:access-lists' in mud_file_contents_dict and 'acl' in mud_file_contents_dict[
            'ietf-access-control-list:access-lists']:
            policy_acl_dict['acls'] = mud_file_contents_dict['ietf-access-control-list:access-lists']['acl']

        return json.dumps(mud_file_contents_dict, indent=4)


    @staticmethod
    def get_mud_file_contents(filename: str) -> str:
        import constants,os

        mud_file_contents = ""

        with open(os.path.join(constants.MUDFILES_DIR, filename)) as f:
            for line in f.readlines():
                mud_file_contents += line + "\n"

        return mud_file_contents


    @staticmethod
    def get_all_urls_from_mud(mud_file_contents: str) -> set:
        """
        Retrieves all URLs contained in the ACLs of the given mud file.
        :param filename: File name of the mud file.
        :return: List of URLs.
        """
        import json

        mud_contents = json.loads(mud_file_contents)
        urls = set()

        for k in mud_contents["ietf-access-control-list:access-lists"]["acl"]:

            for ace in k["aces"]["ace"]:
                try:
                    urls.add(ace["matches"]["ipv4"]["ietf-acldns:dst-dnsname"])
                except KeyError:
                    continue

        return urls


    @staticmethod
    def get_systeminfo_from_mud_file(mud_file_contents: str) -> str:
        import json

        mud_contents = json.loads(mud_file_contents)
        systeminfo = mud_contents['ietf-mud:mud']['systeminfo']

        return systeminfo


    @staticmethod
    def get_mud_file(mud_url: str) -> str:
        from web_scraping.utilities import WebScrapingUtilities
        return WebScrapingUtilities.get_http_content_from_url(mud_url)


    @staticmethod
    def get_mud_files_and_save():
        """
        Retrieves the mud files, given by the URLs in the 'mud_file_urls.csv' file and saves them.
        """
        import ssl, os, constants
        from web_scraping.utilities import WebScrapingUtilities

        ssl._create_default_https_context = ssl._create_unverified_context

        if not os.path.exists(constants.MUDFILES_DIR):
            os.mkdir(constants.MUDFILES_DIR)

        with open(constants.MUD_FILE_URLS_FILE_PATH, "r") as f:
            for line in f.readlines():
                items = line.split(",")
                url = items[0]
                device = items[1].rstrip()

                WebScrapingUtilities.get_http_content_from_url_and_save(url, constants.MUDFILES_DIR, device + ".json")

    @staticmethod
    def get_acl_list_json(acl: str) -> list:
        """
        Retrieve dict object with only the ACL nodes from the string 
        returned by function extract_acls_from_mud_contents
        """
        from json import loads
        return loads(acl)['ietf-access-control-list:access-lists']['acl']
        
    @staticmethod
    def get_acl_from_acl_list_item(acl: list) -> list:
        """
        Retrieve list of ACL entries in object returned by the function
        get_acl_list_json
        """
        return acl["aces"]["ace"]

    @staticmethod
    def get_protocol_name_from_num(num: int) -> str:
        """
        Retrieve the protocol name from the corresponding identifier
        in the MUD file, as specified here:
        https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
        """
        import csv

        protocol_list = []
        with open('data/protocol-numbers.csv', 'r') as csvfile:
            rdr = csv.reader(csvfile, delimiter=',')
            ROI = [row for i, row in enumerate(rdr) if i > 0 and row[0] == str(num)]
            return ROI[0][1]

        return ""
