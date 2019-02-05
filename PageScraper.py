

class PageScraper:
    '''
    A utility class for scraping html from a url and also cleaning the text.
    '''

    @staticmethod
    def get_html_content_from_url(url: str) -> str:
        '''Retrieves the html content of a URL.

        @param url: URL of the content

        @returns: HTML content
        '''
        import urllib.request


        request = urllib.request.urlopen(url)
        bytes = request.read()

        html_content = bytes.decode("utf8")
        request.close()

        print(html_content)

        return html_content

    @staticmethod
    def get_content_from_url_and_save(url: str):
        '''Retrieves the html content of a URL and saves it in the "retrieved text" subfolder.

        @param url: URL of the content

        @returns: HTML content
        '''

        html_content = PageScraper.get_html_content_from_url(url)




        pass



if __name__ == "__main__":
    PageScraper.get_html_content_from_url("https://stackoverflow.com/questions/24153519/how-to-read-html-from-a-url-in-python-3")
