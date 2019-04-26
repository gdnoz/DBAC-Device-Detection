class FingerbankApiResult:
    """
    Wrapper for the result retrieved from the fingerbank api iterrogation.
    """

    device_name = ""
    score = 0

    def __init__(self, device_name: str, score: int):
        self.device_name = device_name
        self.score = score

class FingerbankApi:
    """
    Wrapper for for the Fingerbank API used for device detection based on on dhcp fingerprinting.
    """

    interrogate_endpoint = "https://api.fingerbank.org/api/v2/combinations/interrogate"
    device_endpoint = "https://api.fingerbank.org/api/v2/local_device_applications"
    api_key = "173eaf0e9527bbd5f55e717a5e6b4cfe6bde02a7"

    @staticmethod
    def interrogate(dhcp_fingerprint: list, dhcp_vendor = "", mac = "") -> FingerbankApiResult:
        result = FingerbankApi._get(endpoint=FingerbankApi.interrogate_endpoint, dhcp_fingerprint=",".join(list(map(str,dhcp_fingerprint))), dhcp_vendor= dhcp_vendor, mac=mac)
        return FingerbankApiResult(result['device']['name'],result['score'])

    @staticmethod
    def get_device_from_id(id: int):
        return FingerbankApi._get(endpoint=FingerbankApi.device_endpoint,id=id)

    @staticmethod
    def _get(endpoint:str, **kwargs):
        import requests

        params_dict = kwargs
        params_dict['key'] = FingerbankApi.api_key

        response = requests.get(endpoint, params=params_dict)
        response.raise_for_status()

        return response.json()