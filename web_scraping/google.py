class GoogleCustomSearchAPI:
    api_key = "AIzaSyARQbgHC8noqfizxAmU7B30q8DXw87v37Y"
    custom_search_engine_id = "003252831122657018969:yb1dw3wzz6c"
    endpoint = "https://www.googleapis.com/customsearch/v1"

    exclude_pdf = "+%2Dfiletype%3Apdf"

    @staticmethod
    def search(search_terms: str, exclude_pdf=False) -> list:
        import requests
        from requests import HTTPError


        if exclude_pdf:
            q = search_terms + GoogleCustomSearchAPI.exclude_pdf
        else:
            q = search_terms

        params = \
            {"q": q,
             "cx": GoogleCustomSearchAPI.custom_search_engine_id,
             "key": GoogleCustomSearchAPI.api_key,
             "lr": "lang_en",
             }

        response = requests.get(GoogleCustomSearchAPI.endpoint, params=params)

        try:
            response.raise_for_status()
            return [result_dict['link'] for result_dict in response.json()['items']]
        except KeyError:
            return []
        except HTTPError:
            return []

    @staticmethod
    def search_text(search_terms: str, exclude_pdf=False) -> list:
        import requests
        from requests import HTTPError

        if exclude_pdf:
            q = search_terms + GoogleCustomSearchAPI.exclude_pdf
        else:
            q = search_terms

        params = \
            {"q": q,
             "cx": GoogleCustomSearchAPI.custom_search_engine_id,
             "key": GoogleCustomSearchAPI.api_key,
             "lr": "lang_en",
             }

        response = requests.get(GoogleCustomSearchAPI.endpoint, params=params)

        try:
            response.raise_for_status()
            return [result_dict['title'] + " " + result_dict['snippet'] for result_dict in response.json()['items']]
        except KeyError:
            return []
        except HTTPError:
            return []