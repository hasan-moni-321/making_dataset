import os, zipfile 
import streamlit as st 



########################################################
# Visualize loggings
########################################################
def logging_visualization(log_stream):
    # Scrollable logs container
    logs_html = """
    <div style="height: 300px; overflow-y: auto; overflow-x: hidden; background-color: white; 
                color: black; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
    """ 
    # Append logs dynamically
    if log_stream:
        for log in log_stream:
            logs_html += f"<p>{log}</p>"
    else:
        logs_html += "<p>No logs available.</p>"

    # Close the div
    logs_html += "</div>"
    st.markdown(logs_html, unsafe_allow_html=True)

    # Clear logs button
    if st.button("Clear logs"): 
        log_stream.clear() 
        st.success("Logs cleared.")





#################################################################
# Download dataset
#################################################################
# Function to get the latest files from the "datasets" folder
def get_latest_files(folder_path):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # Sort files by modification time
    files.sort(key=os.path.getmtime, reverse=True)
    # Filter for last CSV and JSON files
    latest_csv = next((f for f in files if f.endswith('.csv')), None)
    latest_json = next((f for f in files if f.endswith('.json')), None)
    return latest_csv, latest_json

# Function to create a zip file with the latest CSV and JSON files
def create_zip_file(csv_file, json_file, zip_filename="latest_csv_json_files.zip"):
    with zipfile.ZipFile(zip_filename, "w") as zipf: 
        if csv_file:
            zipf.write(csv_file, os.path.basename(csv_file))
        if json_file:
            zipf.write(json_file, os.path.basename(json_file))
    return zip_filename


def main_function_download_dataset():
    # Folder path
    folder_path = "datasets"

    # Check if the folder exists
    if not os.path.exists(folder_path):
        st.error(f"Folder '{folder_path}' does not exist!")
        return
    
    # Get the latest CSV and JSON files
    latest_csv, latest_json = get_latest_files(folder_path)

    if not latest_csv and not latest_json:
        st.warning("No CSV or JSON files found in the 'datasets' folder!")
        return

    # Create a zip file containing the latest files
    zip_file_path = create_zip_file(latest_csv, latest_json)

    return zip_file_path



