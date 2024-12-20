<h1 align="center">
Making dataset for training/fine-tuning LLMs model
</h1>

## How to run the project  
1. Open the terminal of your local pc and run the below code.  
   git clone https://github.com/hasan-moni-321/making_dataset.git  
2. Change your current directory to Agent directory using below code.    
   cd making_dataset  
3. Make a virtual environment using below code in ubuntu terminal  
   python3 -m venv venv  
4. Activate the virtual environment using  
   source venv/bin/activate  
5. install the necesary library and dependencies using below code.   
   pip install -r requirements.txt  
6. And finally run the application using below code.  
7. streamlit run main.py      


## Front-End View

![alt text](https://github.com/hasan-moni-321/making_dataset/blob/main/images/Screenshot%20from%202024-12-19%2022-19-55.png) 

## Sample Input 
1. AI in education
2. AI in Healthcare
3. RAG(Retrieval Augmented Generation)
4. AI
5. NLP
6. AI in Business

## Output 
provide a CSV and a json file dataset in the datasets directory. Where 2 columns in csv file, one for Questions and one for Answers. There are only ten rows for each dataset. We can generate more and more row as we want. I make a 10 rows sample dataset because of the simplicity and for quick answer/output/dataset. Same dataset/data in the json file what had in the csv file. 
We can downlaod both the dataset by clicking "Download Latest Files" button. 

## Technology Used  
1. LangFlow (for agent)
2. Pandas (for data preprocessing)
3. Streamlit (for frontend)
4. Groq (API for LLMs model)
5. Llama-3.1-8b-instant (for large language model)

## Challenges 
1. Proper collaboration of multi agent for generating proper question and answer.
2. Bigger csv and json dataset handling within a short time.

## System Achitecture 
1. Two LangFlow agent created in DataStax. One for Question Generation and another one for Answer generation.    I accessed the two agent using LangFlow API in our application. 
2. Three function based agent created. One "Data Cleaning Agent" is used for cleaing the dataset/text in both    questions and answers columns. 2nd one is "Data Formatter Agent" used for formatting the dataset for       
   example, dataframe cration from the dictionary. 3rd one "Dataset validator agent" is created for 
   validating the whole dataset within a short time.
3. Other functional agents like log_activity, logging_visualization, get_latest_files, create_zip_file,       
   data_quality_report, save_dataset_and_report and finally run_flow are created for backend management.
4. After Generating datasets will store in datasets directory in our applicatin.
5. For downloading the csv and json dataset from the UI click "Download Latest Files" button. Both the file will automatically download as a zip file. 

## How to improve accuracy
1. use Google search API
2. use better model like ChatGPT40, Llama3-70B
3. Youtube API and Web search
4. GPT pro

## Future Task 
1. Database for storing the data. For example Vector DataBase.
2. Better UI using HTML, CSS, Bootstrap, Django
3. User Authentication
4. Analytics Dashboard
5. Collecting more data using additional Data Source like Google Search API, Youtube, LinkedIn, Social Media
6. Production base code, Dockerize application, building docker image, CI/CD pipeline, Github Action.  

## Note: 
This is not a production grade application building. For production grade application need so much file and also need huge number of coding line for logging, error handling, setup, pipeline, CI, CD tools, Docker, DockerHub, Github Action, Cloud Service. Within 5 days it is impossible to build a production grade application as I am doing a full time job. 
