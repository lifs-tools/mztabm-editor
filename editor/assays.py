import os
import pandas as pd
import streamlit as st

def compute_assays_form(dataset_idx, datasets_metadata, working_dir):
    st.markdown("## Assays")