class GoogleCustomSearchAPI:
    api_key = "AIzaSyCPpUsEJqELApfL8UpnTJ0zHXPetpSq-a4"
    custom_search_engine_id = "003252831122657018969:yb1dw3wzz6c"
    endpoint = "https://www.googleapis.com/customsearch/v1"

    @staticmethod
    def search(search_terms: str) -> list:
        import requests,json

        headers = {}
        params = \
            {"q": search_terms,
             "cx": GoogleCustomSearchAPI.custom_search_engine_id,
             "key": GoogleCustomSearchAPI.api_key,
             "lr": "lang_en",
             }

        response = requests.get(GoogleCustomSearchAPI.endpoint, params=params)
        response.raise_for_status()
        return [result_dict['link'] for result_dict in response.json()['items']]