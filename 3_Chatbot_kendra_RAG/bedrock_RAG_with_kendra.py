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

def call_chain():
    region = 'us-east-1'
    # Sub in a Kendra index ID that your AWS account credentials has access to
    kendra_index_id = '982ec499-4a49-42e5-b344-2097ab05808b'
    
    retriever = AmazonKendraRetriever(index_id=kendra_index_id,top_k=5,region_name=region)

    llm = Bedrock(
        #client=bedrock,
        model_kwargs={"max_tokens_to_sample":300,"temperature":1,"top_k":250,"top_p":0.999},
        model_id="anthropic.claude-v1"
    )

    prompt_template = """Human: This is a friendly conversation between a human and an AI. 
    The AI is friendly with an energizing and happy personality.  
    The AI is talkative and provides specific details from its context but limits it to 240 tokens.
    If the AI does not know the answer to a question, it truthfully says it 
    does not know.

    Assistant: OK, got it, I'll be a talkative truthful AI assistant..

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

def main() -> None:

    qa = call_chain()

    st.title("Bedrock Q&A")

    current_tool = st.selectbox(
        "Choose Tool:", ["Amazon Bedrock"]
    )

    query = st.text_input("Query:")

    if st.button("Submit Query"):
        with st.spinner("Generating..."):
            if current_tool == "Amazon Bedrock":
                answer = qa({"query": query})
                st.markdown(answer["result"])

                docs = answer["source_documents"]

                with st.expander("Resources"):
                    for doc in docs:
                        doc = str(doc).split("metadata=")[-1]
                        doc = doc + "\n"
                        st.write(doc)

if __name__ == "__main__":
    main()