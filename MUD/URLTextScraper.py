class URLTextScraper:
    blacklist = {"ntp","time","www.example.com"}
    visited_urls = set()
    expansion_urls = set()

    def __init__(self, filename: str):
        self.filename = filename

    def extract_text_from_urls(self) -> str:
        import tldextract
        from MUD.MUDUtilities import MUDUtilities
        from Scraping.WebScrapingUtilities import WebScrapingUtilities

        print("Classifying " + self.filename + "...")
        urls = MUDUtilities.get_all_urls_from_mud(self.filename)
        text = ""

        for url in urls:
            if not (any(element in url for element in self.blacklist) or self._is_url_sub_domain_of_element_in_blacklist(url) or url in self.visited_urls):
                #print(url + " is not blacklisted")
                try:
                    self.visited_urls.add(url)
                    text += WebScrapingUtilities.extract_text_from_url(url,timeout=2)
                except Exception as e:
                    extract_result = tldextract.extract(url)

                    is_top_level_domain = extract_result.suffix and extract_result.domain and not extract_result.subdomain
                    is_sub_domain = extract_result.suffix and extract_result.domain and extract_result.subdomain

                    if is_top_level_domain:
                        self.blacklist.add(url)
                    elif is_sub_domain:
                        self.blacklist.add(url)
                        self.expansion_urls.add(url)

                    continue
            else:
                # Url contained blacklisted item.
                #print(url + " is blacklisted")
                continue


        if (text != ""):
            print()
            print(text)
            print()
        return text

    def _is_url_sub_domain_of_element_in_blacklist(self, url: str) -> bool:
        """
        Checks if the blacklist contains other urls which are different sub domains of the same domain as the input.
        :param url: Input url
        :return:
        """
        import tldextract

        extract_result = tldextract.extract(url)

        if not extract_result.subdomain:
            return False

        for element in self.blacklist:
            res = tldextract.extract(element)

            if res.suffix == extract_result.suffix and \
                res.domain == extract_result.domain and \
                    (not res.subdomain or extract_result.subdomain in res.subdomain):
                return True

        return False




