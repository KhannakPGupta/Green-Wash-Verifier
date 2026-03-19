import streamlit as st

# Safe retrieval of secrets to prevent app crashes
CLIMATIQ_KEY = st.secrets.get("CLIMATIQ_KEY", "MISSING_KEY")
ORS_KEY = st.secrets.get("ORS_KEY", "MISSING_KEY")