import datetime
from datetime import date

import pandas as pd
import streamlit as st

import requests_functions
from utils import BASES, predictions, divide_currencies, DAYS_OF_PREDICTION, BASES_DESCRIPTIONS

TODAY = date.today()
FIFTEEN_DAYS_BEFORE = TODAY - datetime.timedelta(15)
SIXTY_DAYS_BEFORE = TODAY - datetime.timedelta(60)

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
START_DATE = st.date_input("Pick a START date", min_value=SIXTY_DAYS_BEFORE, max_value=FIFTEEN_DAYS_BEFORE)
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
try:
    for k in time_series_dict_to_forecast.keys():
        forecast = predictions(time_series_dict_to_forecast[k])
        st.subheader(
            f"Value of {AMOUNT} {BASE}'s prediction for next {DAYS_OF_PREDICTION} days in {BASES_DESCRIPTIONS[k]} "
            f"currency")
        st.line_chart(forecast['currency'])

except ValueError as e:
    st.write(
        f"Change the date to do the simulations or one of the currencies doesn't have any value to calculate a "
        f"prediction")
