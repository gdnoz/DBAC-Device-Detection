class FocusedScraper:

    from Text_Classification.DeviceClassifier import DeviceClassifier
    endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    api_key = "2be2931b0cfe482b83e1ed8d879f520f"

    def __init__(self, searchterm: str):
        self.searchterm = searchterm

    def first_ten_results(self) -> list:
        return self.search(limit=10)

    def search(self, limit: int) -> list:
        import requests

        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = \
            {"q": self.searchterm,
             "count": limit,
             "textDecorations": True,
             "textFormat": "HTML",
             "setLang" : "en"
             }
        response = requests.get(self.endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_results = [result_dict['url'] for result_dict in response.json()['webPages']['value']]

        return search_results

if __name__ == "__main__":
    import os
    from MUD.URLRelevantTextScraper import URLRelevantTextScraper
    from Text_Classification.DeviceClassifier import DeviceClassifier
    from MUD.MUDUtilities import MUDUtilities

    for filename in os.listdir("/Users/mathiasthomsen/Dropbox/Uni/0_DBAC Thesis/DBAC Device Detection/data/MUD_Files"):
        systeminfo = MUDUtilities.get_systeminfo_from_mud_file(filename)
        print("Classifying based on: " + systeminfo)
        fs = FocusedScraper(systeminfo)

        urls = fs.search(limit=10)

        text = URLRelevantTextScraper(set(urls)).extract_text_from_urls()
        print(DeviceClassifier(0.4).predict_text(text))