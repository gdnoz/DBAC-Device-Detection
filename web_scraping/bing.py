class BingSearchAPI:
    endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    api_key = "0beeb7a3dedf4028bdbb3f8377b5cb5c"

    @staticmethod
    def first_ten_results(search_terms: str, only_html=False) -> list:
        return BingSearchAPI._search(search_terms, limit=10, only_html=only_html)

    @staticmethod
    def _search(search_terms: str, limit: int, only_html=False) -> list:
        import requests

        headers = {"Ocp-Apim-Subscription-Key": BingSearchAPI.api_key}
        params = {"q": search_terms,
             "count": limit,
             "textDecorations": True,
             "setLang" : "en"
             }

        if only_html:
            params.update({"textFormat": "HTML"})

        response = requests.get(BingSearchAPI.endpoint, headers=headers, params=params)
        response.raise_for_status()

        try:
            return [result_dict['url'] for result_dict in response.json()['webPages']['value']]
        except KeyError:
            return []