import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get

def run():
    st.title(" Welcome to my webscraper")

    st.markdown("""
    This app performs webscraping of data from coinafrique over multiples pages. And we can also
    download scraped data from the app directly without scraping them.
    * **Python libraries:** base64, pandas, streamlit, requests, bs4
    * **Data source:** [coinafrique](https://sn.coinafrique.com/) -- [coinafrique](https://sn.coinafrique.com/categorie/terrains).
    """)

    st.write("---")
    st.subheader("📁 Import your scraped data (CSV or Excel)")

    # ---- FILE UPLOADER ----
    uploaded_file = st.file_uploader(
        "Upload a .csv or .xlsx file",
        type=["csv", "xlsx"]
    )

    if uploaded_file:
        # Read CSV
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        # Read Excel
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")
        st.write("### Preview of imported data:")
        st.dataframe(df)

        # Optional: store df in session_state for use in other pages
        st.session_state["imported_data"] = df
