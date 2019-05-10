class RelevantTextScraper:
    """
    Through a list of urls, text is scraped from the urls only if the text is relevant enough for the device_classification problem at hand.
    """
    blacklist = {"ntp","time","www.example.com"}
    visited_urls = set()
    expansion_urls = set()

    def __init__(self, urls: set, noise_threshold: float):
        from device_classification.text_classification import DeviceClassifier
        self.urls = urls
        self.classifier = DeviceClassifier(threshold=noise_threshold)

    def extract_text_from_urls(self) -> str:
        """
        Extracts text from the urls. Text is discarded if it is irrelevant.
        :return: All relevant texts combined into a string.
        """
        import tldextract
        from web_scraping.utilities import WebScrapingUtilities

        relevant_text = ""

        for url in self.urls:
            if not (any(element in url for element in self.blacklist) or self._is_url_sub_domain_of_element_in_blacklist(url) or url in self.visited_urls):
                #print(url + " is not blacklisted")
                try:
                    self.visited_urls.add(url)

                    scraped_text = WebScrapingUtilities.extract_text_from_url(url,timeout=2)

                    classification = self.classifier.predict_text(scraped_text)

                    if classification.predicted_class != "":
                        #print("Sucessful scrape: " + url + " | " +str(device_classification.prediction_probability))
                        relevant_text += scraped_text
                    #else:
                    #    print("Failed scrape: " + url + " | " +str(device_classification.prediction_probability))

                except Exception as ex:
                    if ".pdf" in url: #Failed because url linked to a pdf file. Try again, but handle the pdf case specifically.
                        print("Fetching .pdf")
                        scraped_text = WebScrapingUtilities.get_pdf_content_from_url(url)

                        classification = self.classifier.predict_text(scraped_text)

                        if classification.predicted_class != "":
                            relevant_text += scraped_text

                    #print(url + " caused an Exception.")
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


        #if (relevant_text != ""):
            #print()
            #print(relevant_text)
            #print()
        return relevant_text

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