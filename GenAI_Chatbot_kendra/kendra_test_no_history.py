# from aws_langchain.kendra import AmazonKendraRetriever #custom library
from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.llms.bedrock import Bedrock
from langchain.chains.llm import LLMChain
from langchain.chains import RetrievalQA
import sys
import os


def call_chain():
    region = 'us-east-1'
    kendra_index_id = '982ec499-4a49-42e5-b344-2097ab05808b'
    
    retriever = AmazonKendraRetriever(index_id=kendra_index_id,top_k=5,region_name=region)

    llm = Bedrock(
        #client=bedrock,
        model_kwargs={"max_tokens_to_sample":300,"temperature":1,"top_k":250,"top_p":0.999},
        model_id="anthropic.claude-v1"
    )

    prompt_template = """

    Human: Use the following pieces of context to provide a concise answer to the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context

    Question: {question}

    Assistant:"""

    prompt_template_2 = """Human: This is a friendly conversation between a human and an AI. 
    The AI is talkative and provides specific details from its context but limits it to 240 tokens.
    If the AI does not know the answer to a question, it truthfully says it 
    does not know.

    Assistant: OK, got it, I'll be a talkative truthful AI assistant.

    Human: Here are a few documents in <documents> tags:
    <documents>
    {context}
    </documents>
    Based on the above documents, provide a detailed answer for, {question} 
    Answer "don't know" if not present in the document. 

    Assistant:
    """



    PROMPT = PromptTemplate(
        template=prompt_template_2, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever= retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa

if __name__ == "__main__":
    qa = call_chain()
    query = "What is a solutions architect?"
    result = qa({"query": query})
    #print_ww(result)
    print(result['result'])