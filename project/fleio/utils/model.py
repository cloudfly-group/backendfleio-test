from typing import Dict
from typing import List
from typing import Tuple


def dict_to_choices(dictionary: Dict[str, str]) -> List[Tuple[str, str]]:
    return [(key, dictionary[key]) for key in dictionary]


def choices_to_dict(choices: Tuple[Tuple[str, str]]) -> Dict[str, str]:
    return {choice[0]: choice[1] for choice in choices if len(choices) > 1}


def statuses_dict_to_statuses_choices(dictionary: Dict[str, str]) -> List[Dict[str, str]]:
    """Method that sends statuses as a list for frontend filtering"""
    statuses = list()
    for status, status_display in dictionary:
        statuses.append({
            'display': status_display,
            'value': status
        })
    return sorted(statuses, key=lambda x: x['display'])
