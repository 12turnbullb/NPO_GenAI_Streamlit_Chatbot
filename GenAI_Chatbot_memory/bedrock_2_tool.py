import json

import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
from transformers import Tool
import os

bedrock = boto3.client(service_name='bedrock-runtime')

""" bedrock = boto3.client(
    service_name="bedrock",
    region_name="us-east-1",
    endpoint_url="https://bedrock.us-east-1.amazonaws.com",
) """

""" def bedrock_call(prompt_data):

    body = json.dumps({
        "prompt": prompt_data,
        "max_tokens_to_sample": 300,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    # text
    print(response_body.get('completion')) 
    return response_body.get('completion')


def langchain_call(prompt_data):
    inference_modifier = {
        "max_tokens_to_sample": 4096,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": [],
    }

    textgen_llm = Bedrock(
        model_id="anthropic.claude-instant-v1",
        client=bedrock,
        model_kwargs=inference_modifier,
    )

    response_new = textgen_llm(prompt_data)

    print(response_new)

    return response_new """


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


class AWSGenAITool(Tool):
    name = "well_architected_tool"
    description = "Use this tool for any AWS related question to help customers understand best practices on building on AWS. It will use the relevant context from the AWS Well-Architected Framework to answer the customer's query. The input is the customer's question. The tool returns an answer for the customer using the relevant context."
    inputs = ["text"]
    outputs = ["text"]

    def __call__(self, query):
        # Find docs
        embeddings = BedrockEmbeddings()
        vectorstore = FAISS.load_local("local_index_test", embeddings)
        docs = vectorstore.similarity_search(query)
                
        context = ""

        doc_sources_string = ""
        for doc in docs:
            doc_sources_string += doc.metadata["source"] + "\n"
            context += doc.page_content

        prompt = f"""Human:Use the following pieces of context to answer the question at the end. Give a very detailed, long answer.

        {context}

        Question: {query}
        Assistant:"""
        # print prompt for log
        print("prompt:\n")
        print(prompt)
        print("\nend of prompt\n")

        generated_text = call_bedrock(prompt)
        #print(generated_text)
        #translate
        resp_json = {"ans": str(generated_text), "docs": doc_sources_string}
        return resp_json

