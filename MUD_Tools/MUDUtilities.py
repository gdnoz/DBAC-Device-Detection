

class MUDUtilities:
    """
    A utility class for scraping html from a url and also cleaning the text.
    """

    @staticmethod
    def get_all_urls_from_mud(filename: str) -> list:
        """
        Retrieves all URLs contained in the ACLs of the given mud file.
        :param filename: File name of the mud file.
        :return: List of URLs.
        """
        import os
        import json

        with open(os.path.join(os.path.join(os.getcwd(),"MUD_Files"),filename)) as f:
            mud_contents = json.load(f)
            urls = list()

            for k in mud_contents["ietf-access-control-list:access-lists"]["acl"]:

                for ace in k["aces"]["ace"]:
                    try:
                        urls.append(ace["matches"]["ipv4"]["ietf-acldns:dst-dnsname"])
                    except KeyError:
                        continue

        return urls

    @staticmethod
    def get_mud_files():
        """Retrieves the mud files, given by the URLs in the 'mud_file_urls.csv* file.
        """
        import ssl
        import os
        from Scraping.WebScraper import WebScraper

        ssl._create_default_https_context = ssl._create_unverified_context

        if not os.path.exists(os.path.join(os.getcwd(),"MUD_Files")):
            os.mkdir(os.path.join(os.getcwd(),"MUD_Files"))


        with open("mud_file_urls.csv","r") as f:
            for line in f.readlines():
                items = line.split(",")
                url = items[0]
                device = items[1].rstrip()

                WebScraper.get_content_from_url_and_save(url, os.path.join(os.getcwd(), "MUD_Files"), device + ".json")

if __name__ == "__main__":
    MUDUtilities.get_mud_files()
