import os
import pandas as pd
import streamlit as st

def compute_form(name, dataset_idx, dataset_name, datasets_metadata, editor_config, pd_config, validation_config, working_dir, session_state, on_change_callback_method): 
    file_name = os.path.join(working_dir, f"{name}-{dataset_idx}.csv")
    global_file_name = os.path.join(working_dir, f"{name}-global.csv")
    if session_state['use_global_'+name]:
        if os.path.exists(global_file_name):
            print(f"Loading {name} from", global_file_name)
            df = pd.read_csv(
                global_file_name,
                dtype=pd_config
            )
        else:
            print("Creating new "+name+" dataframe")
            df = pd.DataFrame(data={}, columns=pd_config.keys())
    else:
        if os.path.exists(file_name):
            print("Loading "+name+" from", file_name)
            df = pd.read_csv(
                file_name,
                dtype=pd_config
            )
        elif os.path.exists(global_file_name):
            print("Loading "+name+" from", global_file_name)
            df = pd.read_csv(
                global_file_name,
                dtype=pd_config
            )
        else:
            print("Creating new "+name+" dataframe")
            df = pd.DataFrame(data={}, columns=pd_config.keys())
    
    loaded_df = pd.DataFrame(df)
    pd.DataFrame.reset_index(loaded_df, drop=True, inplace=True)

    edited_df = st.data_editor(
        loaded_df,
        column_config=editor_config,
        use_container_width=True, 
        num_rows="dynamic",
        hide_index=True,
        key=name+"_"+str(dataset_idx)
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        submitted = st.button("Save", help="Save the "+name+".", type="primary", key="save_"+name+"_"+str(dataset_idx))
    with col2:
        set_global_checked = st.checkbox(
            "Use "+name+" for all datasets", 
            help="If checked, will use these "+name+" for all datasets. Will overwrite any previously set "+name+".", 
            value=session_state['use_global_'+name],
            on_change=on_change_callback_method,  #set_global_loaded_df,
            key='default_'+name+'_value_'+str(dataset_idx)
        )
    with col3:
        clear = st.button("Clear", key="clear_"+name+"_"+str(dataset_idx))
    
    if submitted:
        if set_global_checked:
            session_state['use_global_'+name] = True
            print("Saving global "+name+" to", global_file_name)
            edited_df.to_csv(global_file_name, index=False)
        else:
            print("Saving "+name+" to", file_name)
            session_state['use_global_'+name] = False
            edited_df.to_csv(file_name, index=False)
    if clear:
        if set_global_checked and os.path.exists(global_file_name):
            session_state['use_global_'+name] = True
            print("Removing", global_file_name)
            os.remove(global_file_name)
        if os.path.exists(file_name):
            print("Removing", file_name)
            os.remove(file_name)
        edited_df.drop(edited_df.index, inplace=True)
        loaded_df.drop(edited_df.index, inplace=True)