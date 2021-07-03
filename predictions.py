import pandas as pd
from neuralprophet import NeuralProphet, set_random_seed
from pandas import DataFrame

from utils import DAYS_OF_PREDICTION

set_random_seed(0)


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
