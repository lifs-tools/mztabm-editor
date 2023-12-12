from editor.samples import compute_samples_form
from editor.assays import compute_assays_form
from editor.ms_runs import compute_ms_runs_form
#from editor.ols_lookup import ols_lookup

import streamlit as st
import pandas as pd
import os

st.set_page_config(
    layout="wide",
    page_title="Samples Definition - LipidCompass Submission Editor",
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

def compute_samples_tab(submission_id, dataset_idx, dataset_name, datasets_metadata):
    working_dir = st.session_state['working_dir']
    samples_tab, assays_tab, ms_runs_tab = st.tabs(["Samples", "Assays", "MS Runs"])
    with samples_tab:
        compute_samples_form(dataset_idx, datasets_metadata, working_dir)
    with assays_tab:
        compute_assays_form(dataset_idx, datasets_metadata, working_dir)
    with ms_runs_tab:
        compute_ms_runs_form(dataset_idx, datasets_metadata, working_dir)
    
submission_id = None
if 'submission_id' in st.session_state:
    submission_id = st.session_state['submission_id']
    print(f"Using submission id {submission_id}")
else:
    #warn user and stop execution
    st.warning("Could not find a submission id!")
    st.stop()

st.markdown("## Samples")

selected_sheets = []
if 'selected_sheets' in st.session_state:
    selected_sheets = st.session_state['selected_sheets']
else:
    st.session_state['selected_sheets'] = selected_sheets

samples_selected_sheet = st.selectbox(
    'Each selected sheet will be converted to a dataset',
    options=selected_sheets
)

datasets_metadata = {}
if 'datasets_metadata' in st.session_state:
    datasets_metadata = st.session_state['datasets_metadata']
else:
    st.session_state['datasets_metadata'] = datasets_metadata
#mztabid,mztabversion,title,description
st.markdown(samples_selected_sheet)
if samples_selected_sheet != None and samples_selected_sheet in selected_sheets:    
    idx = selected_sheets.index(samples_selected_sheet)
    idx += 1
    if samples_selected_sheet not in datasets_metadata:
        datasets_metadata[samples_selected_sheet] = {}
    compute_samples_tab(
        dataset_idx=idx, 
        dataset_name=samples_selected_sheet, 
        submission_id=submission_id, 
        datasets_metadata=datasets_metadata
    )