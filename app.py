import streamlit as st

import home 
import dashboard
import data_scraping
import webscraper 
import evaluation

# --- CONFIG ---
st.set_page_config(
    page_title="My data appication",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR ---
st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Dashboard",
        "Data Scraping",
        "Using webscraper",
        "Evaluation",
    ]
)



# --- ROUTING ---
if menu == "Home":
    home.run()

elif menu == "Dashboard":
    dashboard.run()
elif menu == "Data Scraping":
    data_scraping.run()
elif menu == "Using webscraper":
    webscraper.run()
elif menu == "Evaluation":
    evaluation.run()