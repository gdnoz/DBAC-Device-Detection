class MUDUtilities():
    @staticmethod
    def get_all_urls_from_mud(filename: str) -> list:
        """
        Retrieves all URLs contained in the ACLs of the given mud file.
        :param filename: File name of the mud file.
        :return: List of URLs.
        """
        import os
        import json

        with open(os.path.join(os.path.join(os.getcwd(),"MUD"),filename)) as f:
            mud_contents = json.load(f)
            urls = list()

            for k in mud_contents["ietf-access-control-list:access-lists"]["acl"]:

                for ace in k["aces"]["ace"]:
                    try:
                        urls.append(ace["matches"]["ipv4"]["ietf-acldns:dst-dnsname"])
                    except KeyError:
                        continue


        return urls

if __name__=="__main__":
    print(MUDUtilities.get_all_urls_from_mud("Amazon Echo.json"))