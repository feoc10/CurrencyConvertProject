import datetime
from functools import lru_cache
import requests
from utils import cleaner_function, bases_verification

# Definitions of requests
DECIMALS = str(2)


@lru_cache(1000)
def request_conversions(base: str, amount: float) -> dict:
    """
    Function to request the latest conversion from a currency
    :param base: currency base to make a conversion
    :param amount: amount to verify the conversion
    :return:
    >>> request_conversions("BRL", 1200)
    {'base': 'BRL', 'date': '2021-04-17', 'rates': {'EUR': 179.22, 'USD': 214.74}}
    """
    symbols = bases_verification(base)
    url = f'https://api.exchangerate.host/latest?base={base}&symbols={symbols}&places={DECIMALS}&amount={amount}'
    response = requests.get(url)
    return cleaner_function(response.json(), ['base', 'date', 'rates'])


@lru_cache(500)
def request_time_series_conversion(base: str, amount: float, start_date: str, end_date: str) -> dict:
    """
    Function to request a time series of conversions from a currency
    :param base: currency base to make a conversion
    :param amount: amount to verify the conversion
    :param start_date: start date to search a conversion
    :param end_date: end date to search a conversion
    :return:
    >>> request_time_series_conversion('BRL', 1200.00, str(datetime.date(2021, 3, 1)), str(datetime.date(2021, 3, 3)))
    {'base': 'BRL', 'rates': {'2021-03-01': {'EUR': 176.5, 'USD': 212.68}, '2021-03-02': {'EUR': 174.95, 'USD': 211.41}, '2021-03-03': {'EUR': 177.01, 'USD': 213.53}}}
    """
    symbols = bases_verification(base)
    url = f'https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}' \
          f'&base={base}&amount={amount}&places={DECIMALS}&symbols={symbols}'
    response = requests.get(url)
    return cleaner_function(response.json(), ['base', 'rates'])



