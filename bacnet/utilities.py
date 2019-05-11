class BacnetUtilities:
    '''
    General utilities for dealing with BACnet classification.
    '''

    @staticmethod
    def get_deviceType_from_query(query_as_json: str) -> str:
        '''
        Retrieves the dscription field from the result of a bacnet object query.
        :param query_as_json: Bacnet object query in json format.
        :return: Description field.
        '''

        import json
        query = json.loads(query_as_json)

        for key in query:
            if BacnetUtilities.is_dict_device_object(query[key]) and 'deviceType' in query[key].keys():
                return query[key]['deviceType']

        return ""

    @staticmethod
    def get_description_from_query(query_as_json: str) -> str:
        '''
        Retrieves the dscription field from the result of a bacnet object query.
        :param query_as_json: Bacnet object query in json format.
        :return: Description field.
        '''

        import json
        query = json.loads(query_as_json)

        for key in query:
            if BacnetUtilities.is_dict_device_object(query[key]) and 'description' in query[key].keys():
                return query[key]['description']

        return ""

    @staticmethod
    def get_vendor_name_from_query(query_as_json: str) -> str:
        '''
        Retrieves the vendorName field from the result of a bacnet object query.
        :param query_as_json: Bacnet object query in json format.
        :return: Vendor name field.
        '''

        import json
        query = json.loads(query_as_json)

        for key in query:
            if BacnetUtilities.is_dict_device_object(query[key]) and 'vendorName' in query[key].keys():
                return query[key]['vendorName']

        return ""

    @staticmethod
    def get_model_name_from_query(query_as_json: str) -> str:
        '''
        Gets the objectName of the device object.
        :param query_as_json:  Bacnet object query in json format.
        :return: objectName of device object.
        '''

        import json
        query = json.loads(query_as_json)

        for key in query:
            if BacnetUtilities.is_dict_device_object(query[key]) and 'modelName' in query[key].keys():
                return query[key]['modelName']

        return ""

    @staticmethod
    def get_device_object_name_from_query(query_as_json: str) -> str:
        '''
        Gets the objectName of the device object.
        :param query_as_json:  Bacnet object query in json format.
        :return: objectName of device object.
        '''

        import json
        query = json.loads(query_as_json)

        for key in query:
            if BacnetUtilities.is_dict_device_object(query[key]) and 'objectName' in query[key].keys():
                return query[key]['objectName']

        return ""

    @staticmethod
    def is_dict_device_object(object_dict: dict) -> bool:
        return object_dict['objectIdentifier'][0] == 'device'

