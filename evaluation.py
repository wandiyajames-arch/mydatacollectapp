import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get


def run():
    st.title("Please give us feedback through the evaluation form!")
    st.write("---")
    st.subheader("Evaluate us")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Google Form")
        st.markdown(
            "<a href='https://forms.gle/bbn1SSAS3fGDFzXJA' target='_blank' class='button'>"
            "<button style='padding:10px 20px; border-radius:8px; background-color:#4285F4; color:white; border:none;'>Open Google Form</button>"
            "</a>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("### KoboToolbox Form")
        st.markdown(
            "<a href='https://ee.kobotoolbox.org/x/vg8RNvcf' target='_blank' class='button'>"
            "<button style='padding:10px 20px; border-radius:8px; background-color:#005F73; color:white; border:none;'>Open Kobo Form</button>"
            "</a>",
            unsafe_allow_html=True
        )
