import os
from editor.data_editor_form import compute_form
import pandas as pd
import streamlit as st

def set_global_publications():
    print("set_global_publications: " + str(st.session_state.use_global_publications))
    # if 'use_global_publications' not in st.session_state:
    #     st.session_state.use_global_publications = False
    
    # if(value != None):
    #     st.session_state.use_global_publications = value

def compute_publications_form(dataset_idx, dataset_name, datasets_metadata, working_dir):
    st.markdown("## Publications")
    
    if 'use_global_publications' not in st.session_state:
        st.session_state.use_global_publications = False

    editor_config = {
        'identifier' : st.column_config.TextColumn('PubMed or DOI (required)', required=True, help="Please enter publications either as pubmed:12345678 or doi:10.1234/12345678")
    }
    pd_config = {
        "identifier": str
    }

    validation_config = {
        "table": {
            "min_rows": 0,
        },
        "columns": {
            "identifier": {
                "regex": r"^(doi\:10\.[1-9][0-9]{3,}(?:\.[1-9][0-9]*)*/(?:(?!['&\"<>])\S)+|pubmed[0-9]+)$"
            }
        }
    }

    compute_form(
        "publications", 
        dataset_idx, 
        dataset_name, 
        datasets_metadata, 
        editor_config, 
        pd_config,
        validation_config,
        working_dir, 
        st.session_state, 
        set_global_publications
    )