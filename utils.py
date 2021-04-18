import copy
import json
import pandas as pd
from pandas import DataFrame
from neuralprophet import NeuralProphet, set_random_seed


"""General definitions"""
BASES = ['USD', 'EUR', 'BRL']
set_random_seed(0)


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


def bases_verification_str(base: str) -> str:
    """
    Verify which base need to be excluded from list of converted currencies
    :param base: Base currency that will be used in convertion
    :return:
    >>> bases_verification_str('BRL')
    'USD,EUR'
    """
    symbols = copy.copy(BASES)
    if base == 'BRL':
        symbols.remove('BRL')
    elif base == 'USD':
        symbols.remove('USD')
    elif base == 'EUR':
        symbols.remove('EUR')

    return ','.join(symbols)


def bases_verification_lst(base: str) -> list:
    """
    Verify which base need to be excluded from list of converted currencies
    :param base: Base currency that will be used in convertion
    :return:
    >>> bases_verification_lst('BRL')
    '[USD,EUR]'
    """
    symbols = copy.copy(BASES)
    if base == 'BRL':
        symbols.remove('BRL')
    elif base == 'USD':
        symbols.remove('USD')
    elif base == 'EUR':
        symbols.remove('EUR')

    return symbols


def divide_currencies(df: DataFrame, base: str) -> dict:
    """
    Divide all currencies into individuals dataframes to make predictions
    :param df: DataFrame with all currencies
    :param base: Used base to make conversion
    :return:
    """
    bases = bases_verification_lst(base)
    df.reset_index(level=0, inplace=True)
    dataframes_dict = dict()
    for currency in bases:
        df_aux = pd.DataFrame()
        df_aux['ds'] = df['index']
        df_aux['y'] = df[currency]
        dataframes_dict[currency] = df_aux
    return dataframes_dict


def predictions(df: DataFrame) -> DataFrame:
    """
    Make predictions about
    :param df: Dataframe to make the predictions
    :return:
    """
    m = NeuralProphet()
    m.fit(df, freq='D')
    future = m.make_future_dataframe(df, periods=7)
    forecast = m.predict(future)
    forecast['ds'] = pd.to_datetime(forecast['ds']).dt.strftime('%Y-%m-%d')
    forecast = forecast.set_index('ds')
    forecast.rename(columns={'yhat1': 'currency'}, inplace=True)
    forecast = forecast.round(2)
    return forecast
