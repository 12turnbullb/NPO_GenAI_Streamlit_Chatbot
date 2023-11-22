import os
import boto3
from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain

bedrock = boto3.client(service_name='bedrock-runtime')

# evironment variables
# export BWB_REGION_NAME="us-east-1"
# export BWB_PROFILE_NAME="default" 
# export BWB_ENDPOINT_URL="https://bedrock.us-east-1.amazonaws.com"
# command to run the app: streamlit run chatbot_app.py --server.port 8080

def get_llm():

    inference_modifier = {
        "max_tokens_to_sample": 4096,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": [],
    }

    llm = Bedrock(
        model_id="anthropic.claude-instant-v1",
        client=bedrock,
        model_kwargs=inference_modifier,
    )


    return llm
        
def get_memory(): #create memory for this chat session
    
    #ConversationSummaryBufferMemory requires an LLM for summarizing older messages
    #this allows us to maintain the "big picture" of a long-running conversation
    llm = get_llm()
    
    memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=4024) #Maintains a summary of previous messages
    
    return memory

def get_chat_response(input_text, memory): #chat client function
    
    llm = get_llm()
    
    conversation_with_summary = ConversationChain( #create a chat client
        llm = llm, #using the Bedrock LLM
        memory = memory, #with the summarization memory
        verbose = True #print out some of the internal states of the chain while running
    )
    
    chat_response = conversation_with_summary.predict(input=input_text) #pass the user message and summary to the model
    
    return chat_response
