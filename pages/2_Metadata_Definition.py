from editor.general import compute_general_settings_form
from editor.contacts import compute_contacts_form
from editor.publications import compute_publications_form
from editor.databases import compute_databases_form
from editor.software import compute_softwares_form
from editor.instruments import compute_instruments_form
from editor.identification_quantification import compute_identification_and_quantification_form
#from editor.ols_lookup import ols_lookup

import streamlit as st
import pandas as pd
import os

st.set_page_config(
    layout="wide",
    page_title="Metadata Definition - LipidCompass Submission Editor",
    page_icon="assets/favicon.ico",
    menu_items={
        'Get Help': 'https://lifs-tools.org/support.html',
        'Report a bug': "https://github.com/lifs-tools/lipidcompass-submissions/issues/new/choose",
        'About': "# This is the mzTab-M creation wizard for LipidCompass."
    }
)

if 'cv_config' in st.session_state:
    print("Initializing OLS Lookup...")
    #ols_lookup = ols_lookup(st.session_state.cv_config['ontologies'], st.session_state.cv_config['static_cv_terms'])
# mzTabm = MzTabM()

def compute_metadata_tab(submission_id, dataset_idx, dataset_name, datasets_metadata):
    working_dir = st.session_state['working_dir']
    general_settings_tab, contacts_tab, publications_tab, instruments_tab, databases_tab, softwares_tab, identification_and_quantification_tab = st.tabs(["General settings", "Contacts", "Publications", "Instruments", "Databases", "Softwares", "Identification and quantification"])    
    with general_settings_tab:
        compute_general_settings_form(submission_id, dataset_idx, dataset_name, datasets_metadata, working_dir)
    with contacts_tab:
        compute_contacts_form(dataset_idx, dataset_name, datasets_metadata, working_dir)
    with publications_tab:
        compute_publications_form(dataset_idx, dataset_name, datasets_metadata, working_dir)
    with instruments_tab:
        compute_instruments_form(dataset_idx, dataset_name, datasets_metadata, working_dir)
    with databases_tab:
        compute_databases_form(dataset_idx, working_dir)  
    with softwares_tab:
        compute_softwares_form(dataset_idx, working_dir)    
    with identification_and_quantification_tab:
        compute_identification_and_quantification_form(dataset_idx, working_dir)
    
submission_id = None
if 'submission_id' in st.session_state:
    submission_id = st.session_state['submission_id']
    print(f"Using submission id {submission_id}")
else:
    #warn user and stop execution
    st.warning("Could not find a submission id!")
    st.stop()

st.markdown("## Metadata")

selected_sheets = []
if 'selected_sheets' in st.session_state:
    selected_sheets = st.session_state['selected_sheets']
else:
    st.session_state['selected_sheets'] = selected_sheets

metadata_selected_sheet = st.selectbox(
    'Each selected sheet will be converted to a dataset',
    options=selected_sheets
)

datasets_metadata = {}
if 'datasets_metadata' in st.session_state:
    datasets_metadata = st.session_state['datasets_metadata']
else:
    st.session_state['datasets_metadata'] = datasets_metadata
#mztabid,mztabversion,title,description
st.markdown(metadata_selected_sheet)
if metadata_selected_sheet != None and metadata_selected_sheet in selected_sheets:    
    idx = selected_sheets.index(metadata_selected_sheet)
    idx += 1
    if metadata_selected_sheet not in datasets_metadata:
        datasets_metadata[metadata_selected_sheet] = {}
    compute_metadata_tab(
        dataset_idx=idx, 
        dataset_name=metadata_selected_sheet, 
        submission_id=submission_id, 
        datasets_metadata=datasets_metadata
    )