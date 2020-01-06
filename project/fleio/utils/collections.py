from typing import Dict


def get_new_or_none(dictionary: Dict, key, previous_value):
    dict_value = dictionary.get(key, None)
    if dict_value == previous_value:
        return None
    else:
        return dict_value
