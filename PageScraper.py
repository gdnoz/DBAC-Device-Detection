

class PageScraper:
    '''
    A utility class for scraping html from a url and also cleaning the text.
    '''

    @staticmethod
    def get_content_from_url(url: str) -> str:
        '''Retrieves the html content of a URL.

        @param url: URL of the content

        @returns: HTML content
        '''
        import urllib.request

        request = urllib.request.urlopen(url)
        bytes = request.read()

        html_content = bytes.decode("utf8")
        request.close()

        return html_content

    @staticmethod
    def get_content_from_url_and_save(url: str, path: str, filename: str):
        '''Retrieves the html content of a URL and saves it in the "retrieved text" subfolder.

        @param url: URL of the content

        @returns: HTML content
        '''

        html_content = PageScraper.get_content_from_url(url)

        import os

        with open(os.path.join(path,filename),"w+") as f:
            f.write(html_content)

        return


    @staticmethod
    def get_mud_urls():
        import ssl
        import os
        ssl._create_default_https_context = ssl._create_unverified_context

        if not os.path.exists(os.path.join(os.getcwd(),"MUD")):
            os.mkdir(os.path.join(os.getcwd(),"MUD"))


        with open("mud_file_urls.csv","r") as f:
            for line in f.readlines():
                items = line.split(",")
                url = items[0]
                device = items[1].rstrip()

                PageScraper.get_content_from_url_and_save(url,os.path.join(os.getcwd(),"MUD"),device+".json")

if __name__ == "__main__":
    PageScraper.get_mud_urls()
