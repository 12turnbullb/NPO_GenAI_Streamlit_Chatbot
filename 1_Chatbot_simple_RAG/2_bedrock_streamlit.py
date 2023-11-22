import json
import sys
import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
#from transformers import Tool
import streamlit as st

bedrock = boto3.client(service_name='bedrock-runtime')

def call_bedrock(prompt):

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

    # titan version
    #results = response_body.get("results")[0].get("outputText")
    return results

def call_rag(query):
    
    embeddings = BedrockEmbeddings()
    vectorstore = FAISS.load_local("local_index_test", embeddings)
    docs = vectorstore.similarity_search(query)
            
    context = ""
    doc_sources_string = ""
    
    
    for doc in docs:
        doc_sources_string += doc.metadata["source"] + "\n"
        context += doc.page_content
        
    prompt = f"""Human:Use the following pieces of context to answer the question at the end. 
    Give a very detailed, long answer.

    {context}

    Question: {query}
    Assistant:"""
    # print prompt for log
    print("prompt:\n")
    print(prompt)
    print("\nend of prompt\n")

    generated_text = call_bedrock(prompt)
    #print(generated_text)
    resp_json = {"ans": str(generated_text), "docs": doc_sources_string}
    
    return resp_json

def app() -> None:

    current_tool = st.selectbox(
        "Choose Tool:", ["Amazon Bedrock"]
    )

    query = st.text_input("Query:")

    if st.button("Submit Query"):
        with st.spinner("Generating..."):
            if current_tool == "Amazon Bedrock":
                answer = call_rag(query)
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
