class WebScrapingUtilities():
    """
    This class contains methods for performing web scraping.
    """
    from typing import Optional
    from requests import Response

    @staticmethod
    def get_content_from_url(url: str) -> str:
        """Retrieves the html content of a URL.

        @param url: URL of the content

        @returns: HTML content
        """
        import urllib.request,ssl

        #Cert's are not veried. Temporary work around.
        gcontext = ssl.SSLContext()

        request = urllib.request.urlopen(url,context=gcontext)
        bytes = request.read()

        html_content = bytes.decode("utf8")
        request.close()

        return html_content

    @staticmethod
    def get_content_from_url_and_save(url: str, path: str, filename: str):
        """Retrieves the html content of a URL and saves it in the "retrieved text" subfolder.

        @param url: URL of the content

        @returns: HTML content
        """
        html_content = WebScrapingUtilities.get_content_from_url(url)

        import os

        with open(os.path.join(path,filename),"w+") as f:
            f.write(html_content)

    @staticmethod
    def extract_text_from_url(url: str, **kwargs) -> str:
        """
        Performs HTTP GET on the url. If the response is valid, the response is cleaned up to reomve any HTML syntax.
        :param url: Url of content.
        :return: Cleaned text of the response.
        """

        try:
            html = WebScrapingUtilities.__http_get(url, timeout=kwargs.get("timeout",None))
        except Exception as e:
            raise e

        if html:
            return WebScrapingUtilities.__clean_html(html)
        else:
            raise TypeError("No HTML retrieved, no content retrieved from URL.")

    @staticmethod
    def extract_links_from_url(url: str) -> list:
        """
        Performs HTTP GET on the url and extracts links from the content of the response.
        :param url: Url of content.
        :return: List of links.
        """
        from bs4 import BeautifulSoup

        try:
            content = WebScrapingUtilities.__http_get(url)
        except Exception as e:
            raise e

        bs = BeautifulSoup(content, 'html.parser')

        anchors = bs.find_all('a')

        all_links = [link.attrs['href'] for link in anchors if 'href' in link.attrs.keys()]

        cleaned_links = list()

        for link in all_links:
            if "http" in link:
                cleaned_links.append(link)
            else:
                cleaned_links.append(url + link)

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

        for script in bs(["script", "style"]): #Remove scripts
            script.decompose()

        for a in bs.find_all('a'): #Remove links
            a.decompose()

        text = bs.get_text()
        lines = (line.strip() for line in text.splitlines())
        phrases = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in phrases if chunk)


    @staticmethod
    def __http_get(url: str, **kwargs) -> Optional[Response]:
        """
        Tries to perform HTTP GET against the given url.
        :param url: Url as string.
        :return: THe content of the reply.
        """
        timeout = kwargs.get("timeout", None)

        if not timeout:
            timeout = 10


        from requests import get, ConnectTimeout
        from requests.exceptions import RequestException
        from contextlib import closing

        fixed_url = ""

        if "//" not in url:
            fixed_url = "http://" + url
        else:
            fixed_url = url

        headers = {"Accept-Language": "en"}

        try:
            with closing(get(fixed_url, stream=True, timeout=timeout, verify=True, headers = headers)) as resp:
                if WebScrapingUtilities.__resp_is_valid(resp):
                    return resp.content
                else:
                    raise TypeError("Response not valid.")

        except ConnectTimeout as e:
            #print('Timeout for request to {0} : {1}'.format(url, str(e)))
            raise e
        except RequestException as e:
            #print('Error during requests to {0} : {1}'.format(url, str(e)))
            raise e


    @staticmethod
    def __resp_is_valid(resp: Response) -> bool:
        """
        :param resp: Response.
        :return: Whether or nor the response is valid.
        """

        try:
            content_type = resp.headers['Content-Type'].lower()
        except KeyError:
            return False

        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)


if __name__ == "__main__":
    # print(WebScraper.extract_text_from_url("https://ipc.tplinkcloud.com/download.php"))
    print(WebScrapingUtilities.get_content_from_url("https://iotanalytics.unsw.edu.au/mud/chromecastUltraMud.json"))
