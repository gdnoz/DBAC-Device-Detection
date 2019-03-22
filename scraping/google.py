class GoogleCustomSearchAPI:
    api_key = "AIzaSyCPpUsEJqELApfL8UpnTJ0zHXPetpSq-a4"
    custom_search_engine_id = "003252831122657018969:yb1dw3wzz6c"
    endpoint = "https://www.googleapis.com/customsearch/v1"

    @staticmethod
    def search(search_terms: str) -> list:
        import requests

        headers = {}
        params = \
            {"q": search_terms,
             "cx": GoogleCustomSearchAPI.custom_search_engine_id,
             "key": GoogleCustomSearchAPI.api_key,
             "lr": "lang_en",
             }

        response = requests.get(GoogleCustomSearchAPI.endpoint, params=params)
        response.raise_for_status()
        search_results = [result_dict['url'] for result_dict in response.json()['webPages']['value']]

        return search_results


if __name__ == "__main__":
    GoogleCustomSearchAPI.search("test search")