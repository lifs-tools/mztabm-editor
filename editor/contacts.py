import os
from editor.data_editor_form import compute_form
import pandas as pd
import streamlit as st

def set_global_contacts():
    print("set_global_contacts: " + str(st.session_state.use_global_contacts))
    # if 'use_global_contacts' not in st.session_state:
    #     st.session_state.use_global_contacts = False
    
    # if(value != None):
    #     st.session_state.use_global_contacts = value

def compute_contacts_form(dataset_idx, dataset_name, datasets_metadata, working_dir):
    st.markdown("## Contacts")

    if 'use_global_contacts' not in st.session_state:
        st.session_state.use_global_contacts = False

    editor_config = {
        'name' : st.column_config.TextColumn('Full Name (required)', required=True),
        'affiliation' : st.column_config.TextColumn('Affiliation', required=True),
        'email' : st.column_config.TextColumn('Email', required=True),
        'orcid' : st.column_config.TextColumn('Orcid', required=False),
    }
    pd_config = {
        "name": str, 
        "affiliation": str, 
        "email": str, 
        "orcid": str
    }

    validation_config = {
        "table": {
            "min_rows": 1,
        },
        "columns": {
            "name": {
                "min_length": 3,
                "max_length": 100,
            },
            "affiliation": {
                "min_length": 3,
                "max_length": 300,
            },
            "email": {
                "regex": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            },
            "orcid": {
                "regex": r"^([0-9]{4}-){3}[0-9]{3}[0-9X]$",
            }
        }
    }

    compute_form(
        "contacts", 
        dataset_idx, 
        dataset_name, 
        datasets_metadata, 
        editor_config, 
        pd_config,
        validation_config, 
        working_dir, 
        st.session_state, 
        set_global_contacts
    )
