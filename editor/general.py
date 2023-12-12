import os
import pandas as pd
import streamlit as st

def compute_general_settings_form(submission_id, dataset_idx, dataset_name, datasets_metadata, working_dir):
    st.markdown(f"## {dataset_name}")
    mztab_head = pd.DataFrame(data={"mztabid":[f"{submission_id}-{dataset_idx}"], "mztabversion":["2.0.0-M"], "title":[None], "description":[None]})
    mztab_head_container = st.empty()

    if "mztab_head" in datasets_metadata[dataset_name]:
        mztab_head = datasets_metadata[dataset_name]["mztab_head"]
    
    mztab_head_container.write(mztab_head)
    with st.form(f"general-settings-{dataset_idx}", clear_on_submit=False):
        mztabid_input = st.text_input(label='mzTab ID', placeholder="Please enter an mzTab ID", value=mztab_head["mztabid"][0])
        title_input = st.text_input(label='Title of your study entry', placeholder="Please enter a title", value=mztab_head["title"][0])
        description_input = st.text_area(label='Description of your study entry', placeholder="Please enter a description", value=mztab_head["description"][0])
        # Every form must have a submit button.
        submitted = st.form_submit_button("Save")
        if submitted:
            mztab_head["mztabid"] = mztabid_input
            mztab_head["title"] = title_input
            mztab_head["description"] = description_input
            datasets_metadata[dataset_name]["mztab_head"] = mztab_head
            print("Saving mztab_head to", os.path.join(working_dir, "mztab_head.csv"))
            mztab_head.to_csv(os.path.join(working_dir, "mztab_head.csv"), index=False)
            mztab_head_container.write(mztab_head)