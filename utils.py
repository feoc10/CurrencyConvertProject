import copy
import json

import pandas as pd
from neuralprophet import NeuralProphet, set_random_seed
from pandas import DataFrame

"""General definitions"""
BASES = sorted(['USD', 'EUR', 'BRL', 'CHF', 'GBP', 'ARS', 'CAD', 'CNY', 'JPY'])
BASES_DESCRIPTIONS = {'USD': "United States Dollar", 'EUR': "Euro", 'BRL': "Brazilian Real", 'CHF': "Swiss Franc",
                      'GBP': "British Pound Sterling", 'ARS': "Argentine Peso", 'CAD': "Canadian Dollar",
                      'CNY': "Chinese Yuan", 'JPY': "Japanese Yen"}
DAYS_OF_PREDICTION = 15
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
    'USD,EUR,CHF,BTC'
    """
    symbols = copy.copy(BASES)
    symbols.remove(base)

    return ','.join(symbols)


def bases_verification_lst(base: str) -> list:
    """
    Verify which base need to be excluded from list of converted currencies
    :param base: Base currency that will be used in convertion
    :return:
    >>> bases_verification_lst('BRL')
    ['USD', 'EUR', 'CHF', 'BTC']
    """
    symbols = copy.copy(BASES)
    symbols.remove(base)
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
    future = m.make_future_dataframe(df, periods=DAYS_OF_PREDICTION)
    forecast = m.predict(future)
    forecast['ds'] = pd.to_datetime(forecast['ds']).dt.strftime('%Y-%m-%d')
    forecast = forecast.set_index('ds')
    forecast.rename(columns={'yhat1': 'currency'}, inplace=True)
    forecast = forecast.round(2)
    return forecast
