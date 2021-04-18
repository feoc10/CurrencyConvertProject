import requests_functions
import streamlit as st
import pandas as pd
import datetime
from datetime import date
from utils import BASES

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
latest_conversion_df = pd.DataFrame(requests_functions.request_conversions(BASE, AMOUNT))

st.subheader("Latest Conversion")
latest_conversion_df

st.write("""""")
START_DATE = st.date_input("Pick a START date", min_value=THIRTY_DAYS_BEFORE, max_value=YESTERDAY)
END_DATE = st.date_input("Pick a END date", max_value=TODAY)

st.write("""""")
st.subheader(f"Values since {START_DATE}")

time_series_conversion_dict = requests_functions.request_time_series_conversion(BASE,
                                                                                AMOUNT, str(START_DATE), str(END_DATE))
time_series_conversion_df = pd.DataFrame(time_series_conversion_dict['rates'])

time_series_conversion_df.T

st.line_chart(time_series_conversion_df.T)
