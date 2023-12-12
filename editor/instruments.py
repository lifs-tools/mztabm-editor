import os
from editor.data_editor_form import compute_form
import pandas as pd
import streamlit as st

def set_global_instruments():
    print("set_global_instruments: " + str(st.session_state.use_global_instruments))

def compute_instruments_form(dataset_idx, dataset_name, datasets_metadata, working_dir):
    st.markdown("## Instruments")

    if 'use_global_instruments' not in st.session_state:
        st.session_state.use_global_instruments = False

    #ols_lookup = ols_lookup(st.session_state.cv_config['ontologies'], st.session_state.cv_config['static_cv_terms'])

    # ols_lookup.

    editor_config = {
        'name' : st.column_config.SelectboxColumn('Instrument Name', required=True),
        'source' : st.column_config.SelectboxColumn('Instrument Source', required=False),
        'analyzer' : st.column_config.SelectboxColumn('Instrument Analyzer', required=False),
        'detector' : st.column_config.SelectboxColumn('Instrument Detector', required=False),
    }
    pd_config = {
        "name": str, 
        "source": str, 
        "analyzer": str, 
        "detector": str
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
            "source": {
                "min_length": 0,
            },
            "analyzer": {
                "min_length": 0,
            },
            "detector": {
                "min_length": 0,
            }
        }
    }

    compute_form(
        "instruments", 
        dataset_idx, 
        dataset_name, 
        datasets_metadata, 
        editor_config, 
        pd_config,
        validation_config, 
        working_dir, 
        st.session_state, 
        set_global_instruments
    )

    # instruments = pd.DataFrame(data={"name":["Please enter an instrument name"], "source":["Please enter a source"], "analyzer":["Please enter an analyzer"], "detector":["Please enter a detector"]})
    # st.write(instruments)
    # with st.form(f"instruments-settings-{dataset_idx}", clear_on_submit=False):
    #     name_input = st.text_input(label='Name', value=instruments["name"][0])
    #     source_input = st.text_input(label='Source', value=instruments["source"][0])
    #     analyzer_input = st.text_input(label='Analyzer', value=instruments["analyzer"][0])
    #     detector_input = st.text_input(label='Detector', value=instruments["detector"][0])
    #     # Every form must have a submit button.
    #     submitted = st.form_submit_button("Save")
    #     if submitted:
    #         instruments["name"] = name_input
    #         instruments["source"] = source_input
    #         instruments["analyzer"] = analyzer_input
    #         instruments["detector"] = detector_input
    #         instruments.to_csv(os.path.join(working_dir, "instruments.csv"), index=False)