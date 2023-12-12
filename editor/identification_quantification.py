import os
import pandas as pd
import streamlit as st

def compute_identification_and_quantification_form(dataset_idx, working_dir):
    st.markdown("## Identification and Quantification")
    #quantification_method,small_molecule-quantification_unit,small_molecule_feature-quantification_unit,small_molecule-identification_reliability,id_confidence_measure[1]
    id_and_quant = pd.DataFrame(data={"quantification_method":["Please enter a quantification method"], "small_molecule-quantification_unit":["Please enter a quantification unit"], "small_molecule_feature-quantification_unit":["Please enter a quantification unit"], "small_molecule-identification_reliability":["Please enter a reliability"], "id_confidence_measure[1]":["Please enter a confidence measure"]})
    st.write(id_and_quant)
    with st.form(f"id_and_quant-settings-{dataset_idx}", clear_on_submit=False):
        quantification_method_input = st.text_input(label='Quantification Method', value=id_and_quant["quantification_method"][0])
        small_molecule_quantification_unit_input = st.text_input(label='Small Molecule Quantification Unit', value=id_and_quant["small_molecule-quantification_unit"][0])
        small_molecule_feature_quantification_unit_input = st.text_input(label='Small Molecule Feature Quantification Unit', value=id_and_quant["small_molecule_feature-quantification_unit"][0])
        small_molecule_identification_reliability_input = st.text_input(label='Small Molecule Identification Reliability', value=id_and_quant["small_molecule-identification_reliability"][0])
        id_confidence_measure_input = st.text_input(label='ID Confidence Measure', value=id_and_quant["id_confidence_measure[1]"][0])
        # Every form must have a submit button.
        submitted = st.form_submit_button("Save")
        if submitted:
            id_and_quant["quantification_method"] = quantification_method_input
            id_and_quant["small_molecule-quantification_unit"] = small_molecule_quantification_unit_input
            id_and_quant["small_molecule_feature-quantification_unit"] = small_molecule_feature_quantification_unit_input
            id_and_quant["small_molecule-identification_reliability"] = small_molecule_identification_reliability_input
            id_and_quant["id_confidence_measure[1]"] = id_confidence_measure_input
            id_and_quant.to_csv(os.path.join("id_and_quant.csv"), index=False)