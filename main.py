import requests, re, os, zipfile 
import streamlit as st 
# import warnings
# warnings.filterwarnings("ignore")

from agent import (run_flow, log_stream) 
from common_function import (main_function_download_dataset,
                             logging_visualization)


def main(): 
    st.title("DataSet Preparation")

    # Input for dataset topic
    message = st.text_area("message", placeholder="Dataset Topic")

    # Dataset preparation button
    if st.button("Make dataset"): 
        if not message.strip():
            st.error("Please enter a message")
            return
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)

            st.markdown("Dataset Prepared! please check the folder")
        except Exception as e: 
            st.error(str(e)) 

    ########################################################
    # Visualize loggings
    ########################################################
    st.subheader("Logs")
    logging_visualization(log_stream)



    ##########################################################
    # Download datasets
    ##########################################################
    st.subheader("Datasets")

    zip_file_path = main_function_download_dataset()

    # Provide the download button for the zip file
    with open(zip_file_path, "rb") as file:
        st.download_button(
            label="Download Latest Files",
            data=file,
            file_name="latest_csv_json_files.zip",
            mime="application/zip"
        )
  

if __name__ == "__main__": 
    main() 
