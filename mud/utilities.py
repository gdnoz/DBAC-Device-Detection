

class MUDUtilities:
    """
    A utility class for scraping html from a url and also cleaning the text.
    """

    @staticmethod
    def get_all_urls_from_mud(filename: str) -> set:
        """
        Retrieves all URLs contained in the ACLs of the given mud file.
        :param filename: File name of the mud file.
        :return: List of URLs.
        """
        import os
        import json

        with open(os.path.join("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/data/MUD_Files",filename)) as f:
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
        import os
        import json

        with open(os.path.join("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/data/MUD_Files",filename)) as f:
            mud_contents = json.load(f)
            systeminfo = mud_contents['ietf-mud:mud']['systeminfo']

        return systeminfo


    @staticmethod
    def get_mud_files():
        """Retrieves the mud files, given by the URLs in the 'mud_file_urls.csv* file.
        """
        import ssl
        import os
        from scraping.utilities import WebScrapingUtilities

        ssl._create_default_https_context = ssl._create_unverified_context

        if not os.path.exists(os.path.join(os.getcwd(),os.path.join("data","MUD_Files"))):
            os.mkdir(os.path.join(os.getcwd(),os.path.join("data","MUD_Files")))


        with open("mud_file_urls.csv","r") as f:
            for line in f.readlines():
                items = line.split(",")
                url = items[0]
                device = items[1].rstrip()

                WebScrapingUtilities.get_content_from_url_and_save(url, os.path.join(os.getcwd(), os.path.join("data", "MUD_Files")), device + ".json")