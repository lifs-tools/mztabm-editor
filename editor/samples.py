import os
import pandas as pd
import streamlit as st

def set_global_samples():
    if 'use_global_samples' not in st.session_state:
        st.session_state.use_global_samples = False
    
    st.session_state.use_global_samples = st.session_state.use_global_samples

def compute_samples_form(dataset_idx, datasets_metadata, working_dir):
    st.markdown("## Samples")