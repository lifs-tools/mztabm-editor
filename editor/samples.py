from functools import partial
import os
from typing import List
import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox
from semlookp_autocomplete import semlookp_autocomplete

def set_global_samples():
    if 'use_global_samples' not in st.session_state:
        st.session_state.use_global_samples = False
    
    st.session_state.use_global_samples = st.session_state.use_global_samples

def getcol(data_frame, column_name, default_value=[]):
    if column_name in data_frame:
        return data_frame[column_name].apply(lambda x: x.split("|"))
    else:
        return default_value

def convert_iri_to_obo_id(response, iri_field=None, fallback_field=None):
    if response is None:
        return fallback_field
    if iri_field is None or response[iri_field] is None:
        return fallback_field
    return response[iri_field].split("/")[-1].replace("_", ":")

def compute_samples_form(dataset, dataset_idx, dataset_name, datasets_metadata, working_dir):
    samples = pd.DataFrame(
        data={
            "name":"Please enter a sample name", 
            "species":["Please enter one or more sample species"], 
            "tissue":["Please enter one or more tissues"], 
            "cell_type":["Please enter one or more cell types"],
            "disease":["Please enter one or more diseases"],
            "custom":["Please enter one or more custom cv parameters"]
        }
    )
    if "samples" in datasets_metadata[dataset_name]:
        samples = datasets_metadata[dataset_name]["samples"]
    else:
        dataset_df = dataset
        print("dataset_df: ", dataset_df)
        #datasets_metadata[dataset_name]["samples"] = samples
        samples["name"] = getcol(dataset_df, "Sample", "")
        samples["species"] = getcol(dataset_df, "Species", "")
        samples["tissue"] = getcol(dataset_df, "Tissue", "")
        samples["cell_type"] = getcol(dataset_df, "CellType", "")
        samples["disease"] = getcol(dataset_df, "Disease", "")
        samples["custom"] = getcol(dataset_df, "Custom", "")
        datasets_metadata[dataset_name]["samples"] = samples
    st.markdown("## Samples")
    st.write(samples)
    for sample_idx in range(len(samples)):
        sample = samples.iloc[sample_idx]
        with st.form(f"sample-{dataset_idx}-{sample_idx}-name", clear_on_submit=False):
            name_input = st.text_input(label='Name', value=sample["name"])
            add_name = st.form_submit_button("Add")
            if(add_name):
                sample["name"] = name_input

        # Species CV term
        with st.form(f"sample-{dataset_idx}-{sample_idx}-species", clear_on_submit=False):
            species = sample["species"]
            st.markdown("<small>Species</small>", unsafe_allow_html=True)
            species_input = semlookp_autocomplete(samples["species"][0], ontologies="ncit,ncbitaxon", rows=1, allow_custom_terms=True, key="species-input-autocomplete")
            st.write(samples["species"])
            add_species = st.form_submit_button("Add")
            if(add_species):
                if(isinstance(species, str)):
                    species = [species_input]
                else:
                    species = species.append(species_input)
                sample["species"] = species
        # Tissue CV term
        with st.form(f"sample-{dataset_idx}-{sample_idx}-tissue", clear_on_submit=False):
            tissue = samples["tissue"]
            st.markdown("<small>Tissue</small>", unsafe_allow_html=True)
            tissue_input = semlookp_autocomplete(samples["tissue"][0], ontologies="bto", rows=1, allow_custom_terms=True, key="tissue-input-autocomplete")
            add_tissue = st.form_submit_button("Add")
            if(add_tissue):
                if(isinstance(tissue, str)):
                    tissue = [tissue_input]
                else:
                    tissue.append(tissue_input)
                sample["tissue"] = tissue
        # Cell Type CV term
        with st.form(f"sample-{dataset_idx}-{sample_idx}-cell-type", clear_on_submit=False):
            cell_type = sample["cell_type"]
            st.markdown("<small>Cell Type</small>", unsafe_allow_html=True)
            cell_type_input = semlookp_autocomplete(samples["cell_type"][0], ontologies="cl", rows=1, allow_custom_terms=True, key="cell-input-autocomplete")
            add_cell_type = st.form_submit_button("Add")
            if(add_cell_type):
                if(isinstance(cell_type, str)):
                    cell_type = [cell_type_input]
                else:
                    cell_type.append(cell_type_input)
                sample["cell_type"] = cell_type
        # Disease CV term
        with st.form(f"sample-{dataset_idx}-{sample_idx}-disease", clear_on_submit=False):
            disease = sample["disease"]
            st.markdown("<small>Disease</small>", unsafe_allow_html=True)
            disease_input = semlookp_autocomplete(samples["disease"][0], ontologies="doid", rows=1, allow_custom_terms=True, key="disease-input-autocomplete")
            add_disease = st.form_submit_button("Add")
            if(add_disease):
                if(isinstance(disease, str)):
                    disease = [disease_input]
                else:
                    disease.append(disease_input)
                sample["disease"] = disease
        # Custom CV term
        with st.form(f"sample-{dataset_idx}-{sample_idx}-custom", clear_on_submit=False):
            custom = sample["custom"]
            st.markdown("<small>Custom</small>", unsafe_allow_html=True)
            custom_input = semlookp_autocomplete(samples["custom"][0], rows=1, allow_custom_terms=True, key="custom-input-autocomplete")
            add_custom = st.form_submit_button("Add")
            if(add_custom):
                if(isinstance(custom, str)):
                    custom = [custom_input]
                else:
                    custom.append(custom_input)
                sample["custom"] = custom

    with st.form(f"sample-{dataset_idx}-{sample_idx}", clear_on_submit=False):
    # Save form
        submitted = st.form_submit_button("Add Sample")
        if submitted:
            samples["name", sample_idx] = name_input
            samples["species", sample_idx] = convert_iri_to_obo_id(species_input, "iri", "name")
            samples["tissue", sample_idx] = convert_iri_to_obo_id(tissue_input, "iri", "name")
            samples["cell_type", sample_idx] = convert_iri_to_obo_id(cell_type_input, "iri", "name")
            samples["disease", sample_idx] = convert_iri_to_obo_id(disease_input, "iri", "name")
            samples["custom", sample_idx] = convert_iri_to_obo_id(custom_input, "iri", "name") 
            datasets_metadata[dataset_name]["samples"] = samples
            print("Writing samples to file: ", os.path.join(working_dir, "samples.csv"))
            samples.to_csv(os.path.join(working_dir, "samples.csv"), index=False)
