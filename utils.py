import copy
import json
import datetime
from datetime import date

# General definitions
BASES = ['USD', 'EUR', 'BRL']


def cleaner_function(json_data: json, returned_keys_list: list) -> dict:
    """
    Function to clean json returned from any request
    :param json_data: json data returned inserted to clean
    :param returned_keys_list:
    :return:
    >>> cleaner_function({'base':'Real','success':'true', 'date':'2021-04-17'}, ['base', 'date'])
    {'base': 'Real', 'date': '2021-04-17'}
    """
    test = {key: value for key, value in dict(json_data).items()
            if key in returned_keys_list}
    return test


def bases_verification(base: str) -> str:
    symbols = copy.copy(BASES)
    if base == 'BRL':
        symbols.remove('BRL')
    elif base == 'USD':
        symbols.remove('USD')
    elif base == 'EUR':
        symbols.remove('EUR')

    return ','.join(symbols)
