import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title="MzTab-M Export - LipidCompass Submission Editor",
    page_icon="assets/favicon.ico",
    menu_items={
        'Get Help': 'https://lifs-tools.org/support.html',
        'Report a bug': "https://github.com/lifs-tools/lipidcompass-submissions/issues/new/choose",
        'About': "# This is the mzTab-M creation wizard for LipidCompass."
    }
)

st.markdown("## Conversion to mzTab-M")

datasets = {}
if 'datasets' in st.session_state:
    datasets = st.session_state['datasets']

metadata_parts = {}
if 'metadata_parts' in st.session_state:
    metadata_parts = st.session_state['metadata_parts']

with st.form("conversion-settings", clear_on_submit=False):
    if datasets == {}:
        st.warning("Please upload a file to begin!")
    
    if metadata_parts == {}:
        st.warning("Please enter metadata to begin!")
    
    submit_disabled = (metadata_parts == {} or datasets == {})
    convert = st.form_submit_button("Create mzTab-M file", disabled=submit_disabled)
    if convert:
        st.info("Converting to mzTab-M...")
