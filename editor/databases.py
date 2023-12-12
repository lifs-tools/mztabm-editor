import os
import pandas as pd
import streamlit as st

def compute_databases_form(dataset_idx, working_dir):
    st.markdown("## Databases")
    databases = pd.DataFrame(data={"cv_term":["Please enter a cv term"],"name":["Please enter a database name"], "prefix": ["Please enter a database prefix"], "version":["Please enter a version"], "uri":["Please enter a location"]})
    st.write(databases)
    with st.form(f"databases-settings-{dataset_idx}", clear_on_submit=False):
        cv_term_input = st.text_input(label='CV Term', value=databases["cv_term"][0])
        name_input = st.text_input(label='Name', value=databases["name"][0])
        prefix_input = st.text_input(label='Prefix', value=databases["prefix"][0])
        version_input = st.text_input(label='Version', value=databases["version"][0])
        uri_input = st.text_input(label='URI', value=databases["uri"][0])
        # Every form must have a submit button.
        submitted = st.form_submit_button("Save")
        if submitted:
            databases["cv_term"] = cv_term_input
            databases["name"] = name_input
            databases["prefix"] = prefix_input
            databases["version"] = version_input
            databases["uri"] = uri_input
            databases.to_csv(os.path.join(working_dir, "databases.csv"), index=False)  