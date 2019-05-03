class JsonCleaner:
    '''
    Utilities for cleaning json after querying bacnet devices for better results when classifying.
    '''

    @staticmethod
    def clean_json_text(json_text: str) -> str:
        '''
        Cleans a json string by removing typical json syntax: "{","}",":", etc.
        :param json_text: The json to be cleaned.
        :return: Cleaned json.
        '''
        json_text.replace()

        return ""