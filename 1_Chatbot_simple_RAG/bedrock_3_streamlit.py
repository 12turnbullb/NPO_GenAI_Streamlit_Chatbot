import json
import sys
import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
#from transformers import Tool
import streamlit as st
from bedrock_2_tool import AWSGenAITool;

well_arch_tool = AWSGenAITool()

bedrock = boto3.client(service_name='bedrock-runtime')

def app() -> None:

    current_tool = st.selectbox(
        "Choose Tool:", ["Amazon Bedrock"]
    )

    query = st.text_input("Query:")

    if st.button("Submit Query"):
        with st.spinner("Generating..."):
            if current_tool == "Amazon Bedrock":
                answer = well_arch_tool(query)
            if type(answer) == dict:
                st.markdown(answer["ans"])
                docs = answer["docs"].split("\n")

                with st.expander("Resources"):
                    for doc in docs:
                        st.write(doc)
            else:
                st.markdown(answer)

def main() -> None:
    st.title("Bedrock Q&A")
    app()

if __name__ == "__main__":
    main()
