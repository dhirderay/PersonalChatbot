from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain import SagemakerEndpoint
from langchain.prompts import PromptTemplate
import pandas as pd
import sqlalchemy
import mysql.connector
import time
import json
import os

region =  "us-east-2" #os.environ["AWS_DEFAULT_REGION"]
endpoint =  "DhirsChatbot-Llama2-7b-Chat" #os.environ["SAGEMAKER_ENDPOINT"]


class ContentHandler(LLMContentHandler):
 content_type = "application/json"
 accepts = "application/json"

 def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
    # Constructing a string format for "inputs"
    input_data = {
        "inputs": f"[{{'Question': 'What does Dhir study?'}}, {{'Question': '{prompt}'}}]",
        "parameters": model_kwargs
    }
    input_str = json.dumps(input_data)
    return input_str.encode('utf-8')
    
 def transform_output(self, output: bytes) -> str:
    response_json = json.loads(output.read().decode("utf-8"))
    return response_json[0]["generated_text"]

#template = "{content}"

#prompt = PromptTemplate.from_template(template)

content_handler = ContentHandler()

llm=SagemakerEndpoint(
     endpoint_name=endpoint, 
     region_name=region, 
     model_kwargs={"max_new_tokens": 1500, "top_p": 0.9, "temperature": 0.2},
     endpoint_kwargs={"CustomAttributes": 'accept_eula=true'},
     content_handler=content_handler
 )

#llm = LlamaCpp(
    #model_path="model/DhirModelQLoRA.gguf",
    #n_ctx=3500,
    #temperature=0.2,
    #max_tokens=1500,
    #top_p=0.5,
    #n_gpu_layers=-1,
    #n_batch=3500,
    #callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    #verbose=True
#)

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()


  #keyword_file_mapping = {
        #'education': 'Education.txt',
        #'experience': 'experience.txt',
        # Add more mappings as needed
    #}

    #for keyword, file_name in keyword_file_mapping.items():
        #if keyword in prompt.lower():
            #file_path = os.path.join('/Users/dhirderay/Desktop/PersonalChatbot', file_name)
            #return read_file_content(file_path)
    #return None

def generate_response(prompt):
    file_content = read_file_content('Education.txt')

    #if file_content:
    full_prompt = f"Dhir's background: {file_content}\nQuestion: {prompt}\n\nAnswer:"
    #else:
        #full_prompt = f"Question: {prompt}\n\nAnswer:"

    for model_output_chunk in llm.stream(full_prompt):
        yield model_output_chunk
