# from aws_langchain.kendra import AmazonKendraRetriever #custom library
from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate
from langchain.llms.bedrock import Bedrock
from langchain.chains.llm import LLMChain
from langchain.chains import RetrievalQA
import sys
import os
import json
import re
import boto3
import streamlit as st

bedrock = boto3.client(service_name='bedrock-runtime')

def call_llm(prompt):

    prompt= f"""Human: This is a friendly conversation between a human and an AI. 
    The AI is talkative and provides specific details.
    If the AI does not know the answer to a question, it truthfully says it 
    does not know.

    Assistant: OK, got it, I'll be a talkative truthful AI assistant.

    Human: Provide a detailed answer for, {prompt}. 

    Assistant:
    """

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 300,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    results = response_body.get('completion')

    return results

def main() -> None:

    st.title("Amazon Bedrock Q&A")

    query = st.text_input("Query:")

    if st.button("Submit Query"):
        with st.spinner("Generating..."):
            results = call_llm(query)
            #print(results)
            st.markdown(results)

if __name__ == "__main__":
    main()