import json
import os
import random
import tempfile
import time
import streamlit as st
import pandas as pd
import numpy as np

from editor.ols_lookup import OLSLookup

st.set_page_config(
    layout="wide", 
    page_title="LipidCompass Submission Editor", 
    page_icon="assets/favicon.ico",
    menu_items={
        'Get Help': 'https://lifs-tools.org/support.html',
        'Report a bug': "https://github.com/lifs-tools/lipidcompass-submissions/issues/new/choose",
        'About': "# This is the mzTab-M creation wizard for LipidCompass."
    }
)

from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
ctx = get_script_run_ctx()
if 'session_id' not in st.session_state:
    print("Setting session ID:", ctx.session_id)
    st.session_state.session_id = ctx.session_id
else:
    print("Retrieving session ID:", st.session_state.session_id)

if 'submission_id' not in st.session_state:
    submission_id = "LCPS-"+st.session_state.session_id
    print(f"Setting submission id {submission_id}")
    st.session_state.submission_id = submission_id

submission_id = st.session_state.submission_id

if 'cv_config' not in st.session_state:
    # reading the data from the file
    with open('config.json') as f:
        data = f.read()
    config = json.loads(data)
    st.session_state.cv_config = config
    ols_lookup = OLSLookup(config['ontologies'], config['static_cv_terms'])
    st.session_state.ols_lookup = ols_lookup

tmp_dir = tempfile.gettempdir()
working_dir = os.path.join(tmp_dir, "lipidcompass", submission_id)
os.makedirs(working_dir, exist_ok=True)
print("Working dir:", working_dir)
st.session_state['working_dir'] = working_dir
# working_dir = os.mkdirs(session_dir).mkdtemp(prefix="LCPS-", suffix="-"+ctx.session_id)
# print(working_dir)
# submission_id = working_dir.split("/")[-1]
# print(submission_id)

st.title("LipidCompass Study Submission Editor")
st.markdown(f"Provisional submission ID: {submission_id}")

# Using "with" notation
with st.sidebar:
    st.markdown("## Datasets")
    if 'datasets' not in st.session_state or st.session_state['datasets'] == {}:
        st.warning("Please upload a file to begin!")
    if 'selected_sheets' not in st.session_state or st.session_state['selected_sheets'] == {}:
        st.warning("Please select a dataset to begin!")
    # with st.spinner("Loading..."):
    #     time.sleep(5)
    # st.success("Done!")
    if 'datasets' in st.session_state and st.session_state['datasets'] != {}:
        for key in st.session_state['selected_sheets']:
            with st.expander(key):
                datasets = st.session_state['datasets']
                rowsMetricColumn, columnsMetricColumn = st.columns(2)
                with rowsMetricColumn:
                    st.metric('Rows', datasets[key].shape[0])
                with columnsMetricColumn:
                    st.metric('Columns', datasets[key].shape[1])
                # if st.button("Edit", key=key):
                #     selected_sheet = key
                # if key in datasets_metadata:
                #     st.write(datasets_metadata[key].keys())
            # st.write(datasets[dataset_key])
        # st.json(datasets)