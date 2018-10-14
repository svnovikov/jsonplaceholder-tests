def check_fields(dict1, dict2):
    """Check all fields of dict1 is in dict2

    :param dict1: dict, first dictionary
    :param dict2: dict, second dictionary
    :return: boolean
    """
    for key, value in dict1.items():
        if isinstance(value, dict):
            if not isinstance(dict2.get(key), dict):
                return False
            check_fields(value, dict2.get(key))
        elif value != dict2.get(key):
            return False
    return True
