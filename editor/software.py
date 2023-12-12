import os
import pandas as pd
import streamlit as st

def compute_softwares_form(dataset_idx, working_dir):
    st.markdown("## Software")
    softwares = pd.DataFrame(data={"name":["Please enter a software name"], "version":["Please enter a version"], "settings":["Please enter settings"]})
    st.write(softwares)
    with st.form(f"softwares-settings-{dataset_idx}", clear_on_submit=False):
        name_input = st.text_input(label='Name', value=softwares["name"][0])
        version_input = st.text_input(label='Version', value=softwares["version"][0])
        settings_input = st.text_input(label='Settings', value=softwares["settings"][0])
        # Every form must have a submit button.
        submitted = st.form_submit_button("Save")
        if submitted:
            softwares["name"] = name_input
            softwares["version"] = version_input
            softwares["settings"] = settings_input
            softwares.to_csv(os.path.join(working_dir, "softwares.csv"), index=False)
