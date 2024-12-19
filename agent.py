import re, requests, logging   
import pandas as pd 
from datetime import datetime 
# from nltk.corpus import stopwords 
# import nltk
# nltk.download('stopwords')


##################################################################
# Setup logger 
##################################################################
logger = logging.getLogger("agent_logger")
logger.setLevel(logging.DEBUG)

#################################################################
# Log handler for external access (e.g., Streamlit)
#################################################################
log_stream = []
def log_activity(message):
    """Log to a global list and logger."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    log_stream.append(log_entry)
    logger.info(message)


#########################################################################################
# Question Generation 
#########################################################################################
def ten_question_generation(message: str)-> dict: 
    """
    Generates Questions using an external API and logs activity.
    """
    # define variables 
    BASE_API_URL = "https://api.langflow.astra.datastax.com"
    LANGFLOW_ID = "b06b7bac-aa20-45b3-a387-481bae5fc0ff"
    FLOW_ID = "be452509-1dfd-40f0-9103-d1d63b4eb64c"
    APPLICATION_TOKEN = "AstraCS:XMpcYBeGsFpNEvpJYGyrguIN:0a857ab678001d655aae80bdd14ab490b705d1c407f35731f84920278b25b691"
    ENDPOINT = "question_generation_endpoint" # The endpoint name of the flow

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    
    log_activity("Preparing API call for Question generation.")
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        log_activity("Question Generation API call successful.")
        #log_activity(f"Question Generation API response: {response.json()}")
        return response.json()
    except Exception as e: 
        log_activity(f"An unexpected error occurred for question generation : {e}")
    
    return {"error": "Failed to get a response from the Question Generatin API"}



###################################################################
# Answer generation 
###################################################################
Base_API_URL_Answer = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID_Answer = "b06b7bac-aa20-45b3-a387-481bae5fc0ff"
FLOW_ID_Answer = "7aeda475-7369-4177-b58d-95e85876e5bc"
APPLICATION_TOKEN_answer = "AstraCS:pejxgzjPZNIdpsyyNvCMCUge:f4a62cd409a6589f244923066528e45cb53f79069bb7ff5d7b48108d92361658"
ENDPOINT_answer = "answer_generation" # The endpoint name of the flow

def answer_generation(message: str) -> dict:
    """
    Generates an answer using an external API and logs activity.
    """
    api_url = f"{Base_API_URL_Answer}/lf/{LANGFLOW_ID_Answer}/api/v1/run/{ENDPOINT_answer}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat", 
    }

    headers = {"Authorization" : "Bearer " + APPLICATION_TOKEN_answer, "Content-Type": "application/json"}
    
    log_activity("Preparing API call for answer generation.")
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        log_activity("Answer Generation API call successful.")
        #log_activity(f"Answer Generation API response: {response.json()}")
        return response.json()
    except Exception as e: 
        log_activity(f"An unexpected error occurred for answer generation : {e}")
    
    return {"error": "Failed to get a response from the Answer Generatin API"}


############################################################
# Data cleaning function 
############################################################
def clean_text_data(text):
    log_activity("Starting column data cleaning.")
    try:
        row = str(text)
        row = row.lower() 
        row = row.replace("\n", " ")
        row = row.replace("\t", " ")  
        row = re.sub(r'<.*?>', '', row) # remove html tag 
        row = re.sub(r'\s+', ' ', row).strip() # remove extra white space

        # Removing stop words
        # stop_words = set(stopwords.words('english'))
        # row = row.split()
        # row = [w for w in row if not w in stop_words]
        # row = " ".join(row) 
        log_activity("Successfully column data cleaned") 
        #log_activity(f"Cleaned data: {row}") 
        return row
    except Exception as e:
        log_activity(f"An unexpected error occurred for cleaning data: {e}")

    return {"error": "Failed to clean data, from the data cleaning function"}


##############################################################
# Data formatting agent 
##############################################################
# define a dictionary 
dictionary_data = {"questions": [], 
                   "answers": []
                  }
def data_formatter():
    try:
        # dictionary to dataframe  
        log_activity("Converting dictionary into dataframe") 
        df = pd.DataFrame(dictionary_data)
        return df 
    except Exception as e: 
        log_activity(f"An unexpected error occurred for data formatting: {e}")

    return {"error": "Failed to format data, from the data formatter function"}


###############################################################
# Data validator agent 
###############################################################
def data_validator(df): 
    # Check for missing values
    missing_summary = df.isnull().sum() 
    # Percentage of missing values
    missing_percentage = (df.isnull().sum() / len(df)) * 100 

    # drop rows with missing values 
    try:
        log_activity("dropping null values ") 
        df = df.dropna() 
        log_activity("Null value dropped successfully")  

        # Check for duplicates
        duplicates = df.duplicated()

        # Drop duplicate rows 
        log_activity("dropping duplicated data")  
        df = df.drop_duplicates()
        log_activity("duplicated data dropped successfully ")  

        # Convert data types if necessary
        log_activity("converting data type to string")
        df['questions'] = df['questions'].astype('str') 
        df['answers'] = df['answers'].astype('str') 
        log_activity("successfully converted data type to string")
        return df
    
    except Exception as e: 
        log_activity(f"An unexpected error occurred for dropping null values : {e}")

    return {"error": "Failed to validate data, from the data validation function"}

     

#################################################################
# Data quality report 
#################################################################
def data_quality_report(df):
    log_activity("Data quality report generation.")
    try:
        report = {
            "missing_values": df.isnull().sum(),
            "missing_percentage": (df.isnull().sum() / len(df)) * 100,
            "duplicates": df.duplicated().sum(),
            "data_types": df.dtypes
        }
        return pd.DataFrame(report)
    except Exception as e: 
        log_activity(f"An unexpected error occurred for data quality report : {e}")

    return {"error": "Failed to generate data quality report, from the data quality report function"}

###############################################################
# Dataset Saving 
###############################################################
def save_dataset_and_report(df, report):
    try:
        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(current_time)
        # Save dataset in csv
        try: 
            log_activity("Fully prepared csv dataset file saving")
            df.to_csv(f"datasets/fully_prepared_dataset_{current_time}.csv", index=False) 
            log_activity("Fully prepared csv dataset saved") 
        except Exception as e: 
            log_activity(f"Failed to save CSV dataset: {e}")
        
        # # Save data quality report in csv 
        # try:
        #     log_activity("Data quality report file saving.")
        #     report.to_csv(f"datasets/data_quality_report_{current_time}.csv", index=False)
        #     log_activity("Data quality report file saved.") 
        # except Exception as e: 
        #     log_activity(f"Failed to save data quality report: {e}")

        # Save dataset in JSON 
        try:
            log_activity("Fully prepared json dataset file saving")
            df.to_json(f"datasets/fully_prepared_dataset_{current_time}.json") 
            log_activity("Fully prepared csv dataset saved") 
        except Exception as e: 
            log_activity(f"Failed to save JSON dataset: {e}")

        print("Dataset saving process completed with logs.") 
    except Exception as e: 
        log_activity(f"An unexpected error occurred for dataset saving : {e}")

    
############################################################
# Define run_flow function for calling other function
############################################################
def run_flow(input_str): 
    # Question generation function call     
    output_json = ten_question_generation(input_str)
    response_questions = output_json["outputs"][0]["outputs"][0]["results"]["message"]["text"] 
    questions = re.findall(r'.*?\?', response_questions) 

    # Answer generation for each question  
    for question in questions: 
        # calling the function
        return_answer = answer_generation(question) 
        response_answer = return_answer["outputs"][0]["outputs"][0]["results"]["message"]["text"] 
        
        # appending data to dictionary_data
        dictionary_data['questions'].append(question)  
        dictionary_data['answers'].append(response_answer) 

    # Calling data formatter 
    df = data_formatter() 

    # Calling data cleaner 
    df['questions'] = df['questions'].apply(lambda x: clean_text_data(x)) 
    df['answers'] = df['answers'].apply(lambda x: clean_text_data(x)) 

    # Calling data validator 
    df = data_validator(df)

    # Calling data quality check 
    df_data_quality = data_quality_report(df)

    # Saving the dataset
    save_dataset_and_report(df, df_data_quality) 
