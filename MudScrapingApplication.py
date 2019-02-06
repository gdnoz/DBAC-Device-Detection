import os
from WebScraper import WebScraper
from MUDUtilities import MUDUtilities
import re


path = os.path.join(os.getcwd(), "MUD")

for filename in os.listdir(path):
    with open(os.path.join(path, filename), "r") as f:
        urls_in_mud_file = MUDUtilities.get_all_urls_from_mud(filename)

        for url in urls_in_mud_file:
            print(filename+": "+url+":"+"\n")
            search = re.match('(?:http|https)://', url)

            try:
                if search:
                    print(WebScraper.extract_links_from_url(url))
                else:
                    print(WebScraper.extract_links_from_url("http://"+url))

                print()
            except Exception as e:
                print(e)
                print()
                continue


