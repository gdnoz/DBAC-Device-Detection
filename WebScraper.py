class WebScraper():
    """
    This class contains methods for performing web scraping.
    """
    from typing import Optional
    from requests import Response

    @staticmethod
    def http_get(url: str) -> Optional[Response]:
        """
        Tries to perform HTTP GET against the given url.
        :param url: Url as string.
        :return: THe content of the reply.
        """

        from requests import get
        from requests.exceptions import RequestException
        from contextlib import closing
        from bs4 import BeautifulSoup

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
    print(WebScraper.http_get("http://ipc.tplinkcloud.com"))