from neuralprophet import NeuralProphet

import requests_functions
import streamlit as st
import pandas as pd
import datetime
from datetime import date
from utils import BASES, predictions, divide_currencies

TODAY = date.today()
YESTERDAY = TODAY - datetime.timedelta(1)
THIRTY_DAYS_BEFORE = TODAY - datetime.timedelta(30)

st.set_page_config(page_title="Currency conversion using Exchangerate API",
                   layout="centered",
                   initial_sidebar_state="expanded")

st.title("Currency conversion using Exchangerate API")
st.write("""""")
st.write("""""")
st.write("""""")

BASE = st.radio("Pick a base currency", BASES)
st.write("""""")
AMOUNT = st.number_input("Amount to be converted:", step=100.0, min_value=100.0)
st.subheader("Latest Conversion")
"""Get the latest conversion of currency available"""
latest_conversion_df = pd.DataFrame(requests_functions.request_conversions(BASE, AMOUNT))
latest_conversion_df

st.write("""""")
START_DATE = st.date_input("Pick a START date", min_value=THIRTY_DAYS_BEFORE, max_value=YESTERDAY)
END_DATE = st.date_input("Pick a END date", max_value=TODAY)

st.write("""""")
st.subheader(f"Values since {START_DATE}")
"""Show the last few days of conversion of currency"""

time_series_conversion_df = requests_functions.request_time_series_conversion(BASE,
                                                                              AMOUNT, str(START_DATE), str(END_DATE))
"""Presenting the return time series"""
time_series_conversion_df
st.subheader(f"Timeline since {START_DATE}")
st.line_chart(time_series_conversion_df)

st.write("""""")
st.subheader(f"Predictions")
"""Make some predictions to these conversions"""
time_series_dict_to_forecast = divide_currencies(time_series_conversion_df, BASE)
for k in time_series_dict_to_forecast.keys():
    forecast = predictions(time_series_dict_to_forecast[k])
    st.subheader(f"Value of {AMOUNT}{BASE}'s prediction for next 7 days in {k} currency")
    st.line_chart(forecast['currency'])

