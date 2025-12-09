import streamlit as st

def run():
    st.title("Settings")
    option = st.selectbox("Choisir une option :", ["Option A", "Option B", "Option C"])
    st.write(f"Option sélectionnée : {option}")
