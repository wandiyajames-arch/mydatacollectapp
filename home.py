import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get


def run():
    st.title("Welcome to AfriDataApp")
    st.markdown("<h1 style='text-align: center; color: black;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)

    st.markdown("""
    This app performs webscraping of data from coinafrique over multiples pages. And we can also
    download scraped data from the app directly without scraping them.
    * **Python libraries:** base64, pandas, streamlit, requests, bs4
    * **Data source:** [coinafrique](https://sn.coinafrique.com/) -- [coinafrique](https://sn.coinafrique.com/categorie/).
    """)