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

def app(multilingual) -> None:

    current_tool = st.selectbox(
        "Choose Tool:", ["Amazon Bedrock"]
    )

    query = st.text_input("Query:")

    translation_language = multilingual

    if st.button("Submit Query"):
        with st.spinner("Generating..."):
            if current_tool == "Amazon Bedrock":
                answer = well_arch_tool(query, translation_language)
            if type(answer) == dict:
                st.markdown(answer["ans"])
                docs = answer["docs"].split("\n")

                with st.expander("Resources"):
                    for doc in docs:
                        st.write(doc)
            else:
                st.markdown(answer)

def main(multilingual) -> None:
    st.title("Bedrock Q&A")
    app(multilingual)

if __name__ == "__main__":
    multilingual = bool(int(sys.argv[1]))
    print('multilingual: ' + str(multilingual))
    main(multilingual)

# streamlit run file.py 1 

# 1 = true for multilingual
# 2 = false for multilingual


# why do we need this language piece?