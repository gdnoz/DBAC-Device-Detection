class WebScrapingUtilities():
    """
    This class contains methods for performing web web_scraping.
    """
    from typing import Optional
    from requests import Response

    @staticmethod
    def get_content_from_url(url: str) -> bytes:
        """Retrieves the byte content of a URL.

        @param url: URL of the content

        @returns: Byte content
        """
        import urllib.request,ssl

        #Cert's are not veried. Temporary work around.
        gcontext = ssl.SSLContext()

        bytes = None

        try:
            request = urllib.request.urlopen(url,context=gcontext)
            bytes = request.read()
            request.close()
        except Exception as e:
            print(e)

        return bytes

    @staticmethod
    def get_http_content_from_url(url: str) -> str:
        '''
        Retrives the byte content from the url and decodes to utf-8 format.
        :param url: URL of the content
        :return: HTTP content
        '''
        bytes = WebScrapingUtilities.get_content_from_url(url)

        html_content = bytes.decode("utf8")
        return html_content

    @staticmethod
    def get_http_content_from_url_and_save(url: str, path: str, filename: str):
        """Retrieves the html content of a URL and saves it in the "retrieved text" subfolder.

        @param url: URL of the content

        @returns: HTML content
        """
        html_content = WebScrapingUtilities.get_http_content_from_url(url)

        import os

        with open(os.path.join(path,filename),"w+") as f:
            f.write(html_content)

    @staticmethod
    def get_pdf_content_from_url(url: str) -> str:
        '''
        Retrives the byte content of a pdf file specified by the url.
        :param url:  URL of pdf content
        :return: PDF content
        '''

        byte_content = WebScrapingUtilities.get_content_from_url(url)

        if byte_content is None:
            print(".pdf not retrieved...")
            return ""
        return PdfToTextConverter.pdf_to_text(byte_content)

    @staticmethod
    def extract_text_from_url(url: str, **kwargs) -> str:
        """
        Performs HTTP GET on the url. If the response is valid, the response is cleaned up to reomve any HTML syntax.
        :param url: Url of content.
        :return: Cleaned text of the response.
        """

        html = None

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

        headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        }

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

class PdfToTextConverter:
    @staticmethod
    def pdf_to_text(byte_content: bytes) -> str:
        import web_scraping.pdf2txt
        import os,constants

        temp_pdf_file_path = os.path.join(constants.TEMP_FOLDER,"temp.pdf")
        temp_output_file_path = os.path.join(constants.TEMP_FOLDER,"temp.txt")
        output = ""

        if not os.path.exists(constants.TEMP_FOLDER):
            os.makedirs(constants.TEMP_FOLDER)


        with open(temp_pdf_file_path, 'wb') as fp:
            fp.write(byte_content)

        try:
            web_scraping.pdf2txt.extract_text([temp_pdf_file_path],temp_output_file_path)
        except Exception as e:
            print(e)
            print("Skipping pdt2text...")

        with open(temp_output_file_path, 'r+') as f:
            for line in f.readlines():
                output += line

        for root, dirs, files in os.walk(constants.TEMP_FOLDER, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        return output

if __name__ == "__main__":
    test = WebScrapingUtilities.get_content_from_url("http://f.licitationen.dk/2ans3fldwwje02ca.pdf")
    PdfToTextConverter.pdf_to_text(test)
