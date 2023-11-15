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

def call_chain():
    region = 'us-east-1'
    kendra_index_id = '8165abf0-f489-4a1f-9908-48bd4e59a747'
    # Eckerd docs - '8165abf0-f489-4a1f-9908-48bd4e59a747'
    # SO docs - '982ec499-4a49-42e5-b344-2097ab05808b'
    
    retriever = AmazonKendraRetriever(index_id=kendra_index_id,top_k=5,region_name=region)

    llm = Bedrock(
        #client=bedrock,
        model_kwargs={"max_tokens_to_sample":300,"temperature":1,"top_k":250,"top_p":0.999},
        model_id="anthropic.claude-v1"
    )

    prompt_template = """Human: This is a friendly conversation between a human and an AI. 
    The AI is a friendly volunteer support leader with an energizing and happy personality.  
    The AI is talkative and provides specific details from its context but limits it to 240 tokens.
    If the AI does not know the answer to a question, it truthfully says it 
    does not know.

    Assistant: OK, got it, I'll be a talkative truthful AI assistant with the goal of helping volunteers.

    Human: Here are a few documents in <documents> tags:
    <documents>
    {context}
    </documents>
    Based on the above documents, provide a detailed answer for, {question} 
    Answer "don't know" if not present in the document. 

    Assistant:
    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Try an alterate chain that uses the sources in the response. 
    # https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever= retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa

def call_llm(prompt):

    prompt_input = f"""Human: This is a friendly conversation between a human and an AI. 
    The AI is a friendly volunteer support leader with an energizing and happy personality.  
    The AI is talkative and provides specific details but limits it to 240 tokens.
    If the AI does not know the answer to a question, it truthfully says it 
    does not know.

    Assistant: OK, got it, I'll be a talkative truthful AI assistant with the goal of helping volunteers.

    Human: Provide a detailed answer for, {prompt}. 

    Assistant:
    """

    prompt_broad = f"""Human: You are a friendly assistant to a 7 year old. 
    Talk in terms a 7 year old would understand. {prompt}
    
    Assistant:"""

    prompt_input_os = f"""Human: Provide supportive coaching to a 7 year old. 
    Maintain an encouraging demeanor and friendly personality. 
    Speak in terms that a 7 year old would understand, and be funny!
    You are encouraged to ask questions at the end of your response. 
    Answer the following question with a concise answer.
    Question: {prompt}
    Assistant:
    """

    body = json.dumps({
        "prompt": prompt_broad,
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

    st.image("./logo.png", width=300)
    st.title("Eckerd Connects Virtual Coach")

    current_tool = st.selectbox(
        "Choose Tool:", ["Open LLM", "RAG LLM"]
    )

    query = st.text_input("Query:")

    if st.button("Submit Query"):
        with st.spinner("Generating..."):
            if current_tool == "RAG LLM":
                qa = call_chain()
                answer = qa({"query": query})
                st.markdown(answer["result"])

                docs = answer["source_documents"]

                with st.expander("Resources"):
                    for doc in docs:
                        doc = str(doc).split("metadata=")[-1]
                        doc = doc + "\n"
                        st.write(doc)
            elif current_tool == "Open LLM":
                results = call_llm(query)
                #print(results)
                st.markdown(results)

if __name__ == "__main__":
    main()