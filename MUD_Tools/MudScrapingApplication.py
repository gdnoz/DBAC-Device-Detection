import os
import re

from MUD_Tools.MUDUtilities import MUDUtilities
from Scraping.WebScraper import WebScraper

path = os.path.join(os.getcwd(), "MUD_Files")
textfolder = "MUDTexts"

if not os.path.exists(textfolder):
    os.mkdir(textfolder)

textpath = os.path.join(os.getcwd(),textfolder)

black_listed = ["ntp"]

for filename in os.listdir(path):
    with open(os.path.join(path, filename), "r") as f:
        urls_in_mud_file = MUDUtilities.get_all_urls_from_mud(filename)

        text = ""

        for url in urls_in_mud_file:
            if any(item in url for item in black_listed):
                continue

            search = re.match('(?:http|https)://', url)

            try:
                if not search:
                    url = "http://"+url

                text += "MAIN SITE: " + url +" \n\n"
                text += WebScraper.extract_text_from_url(url)
                urls = WebScraper.extract_links_from_url(url)

                for url1 in urls:
                    text += "\n\nDERIVED SITE: " + url1 +" \n\n"
                    text += WebScraper.extract_text_from_url(url1)

            except Exception as e:
                print(e)
                continue

        if text is not "":
            with open(os.path.join(textpath,filename), "w+") as f1:
                f1.write(text)





