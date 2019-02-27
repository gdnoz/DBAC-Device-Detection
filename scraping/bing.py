class BingSearchAPI:
    endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    api_key = "2be2931b0cfe482b83e1ed8d879f520f"

    @staticmethod
    def first_ten_results(search_terms: str) -> list:
        return BingSearchAPI._search(search_terms, limit=10)

    @staticmethod
    def _search(search_terms: str, limit: int) -> list:
        import requests

        headers = {"Ocp-Apim-Subscription-Key": BingSearchAPI.api_key}
        params = \
            {"q": search_terms,
             "count": limit,
             "textDecorations": True,
             "textFormat": "HTML",
             "setLang" : "en"
             }

        response = requests.get(BingSearchAPI.endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_results = [result_dict['url'] for result_dict in response.json()['webPages']['value']]

        return search_results