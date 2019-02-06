class WebScraper():
    """
    This class contains methods for performing web scraping.
    """
    from typing import Optional
    from requests import Response

    @staticmethod
    def extract_text_from_url(url: str) -> str:
        """
        Performs HTTP GET on the url. If the response is valid, the response is cleaned up to reomve any HTML syntax.
        :param url: Url of content.
        :return: Cleaned text of the response.
        """

        return WebScraper.__clean_html(WebScraper.__http_get(url))

    @staticmethod
    def extract_links_from_url(url: str) -> list:
        from bs4 import BeautifulSoup

        content = WebScraper.__http_get(url)
        bs = BeautifulSoup(content, 'html.parser')

        all_links = [link.attrs['href'] for link in bs.find_all('a')]

        cleaned_links = list()

        for link in all_links:
            if "http" in link:
                cleaned_links.append(link)
            else:
                cleaned_links.append(url+link)

        return cleaned_links


    @staticmethod
    def __clean_html(html: Response) -> str:
        """
        Takes the html content of a response and cleans it removing any relevant HTML syntax.
        :param html: HTML content of a response.
        :return: Cleaned HTML content.
        """

        from bs4 import BeautifulSoup
        bs = BeautifulSoup(html, 'html.parser')

        for script in bs(["script", "style"]):
            script.decompose()

        text = bs.get_text()
        lines = (line.strip() for line in text.splitlines())
        phrases = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in phrases if chunk)


    @staticmethod
    def __http_get(url: str) -> Optional[Response]:
        """
        Tries to perform HTTP GET against the given url.
        :param url: Url as string.
        :return: THe content of the reply.
        """

        from requests import get
        from requests.exceptions import RequestException
        from contextlib import closing

        try:
            with closing(get(url, stream=True)) as resp:
                if WebScraper.__resp_is_valid(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

    @staticmethod
    def __resp_is_valid(resp: Response) -> bool:
        """
        :param resp: Response.
        :return: Whether or nor the response is valid.
        """

        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)




if __name__ == "__main__":
    #print(WebScraper.extract_text_from_url("https://ipc.tplinkcloud.com/download.php"))
    print(WebScraper.extract_links_from_url("http://ipc.tplinkcloud.com"))