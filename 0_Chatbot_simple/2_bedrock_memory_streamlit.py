import json
import sys
import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
#from transformers import Tool
import streamlit as st
import bedrock_memory_lib as glib #reference to local lib script

# need to install the anthropic library
# pip install anthropic

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
    st.title("Bedrock Q&A")

    if 'memory' not in st.session_state: #see if the memory hasn't been created yet
        st.session_state.memory = glib.get_memory() #initialize the memory


    if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
        st.session_state.chat_history = [] #initialize the chat history


    #Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
    for message in st.session_state.chat_history: #loop through the chat history
        with st.chat_message(message["role"]): #renders a chat line for the given role, containing everything in the with block
            st.markdown(message["text"]) #display the chat content


    input_text = st.chat_input("Chat with your bot here") #display a chat input box

    if input_text: #run the code in this if block after the user submits a chat message
        docs = []
        answer = call_llm(input_text)
        #answer = natgeo_tool(input_text, 0)
        print(answer)
        if type(answer) == dict:
            the_prompt = answer["ans"]
            docs = answer["docs"].split("\n")
        else:
            the_prompt = answer
        with st.chat_message("user"): #display a user chat message
            st.markdown(input_text) #renders the user's latest message

        #if using Claude, need to append Assistant:
        the_prompt = "\n\nHuman: " + the_prompt + "\n\nAssistant:"
        
        st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
        
        chat_response = glib.get_chat_response(input_text=the_prompt, memory=st.session_state.memory) #call the model through the supporting library
            
        with st.chat_message("assistant"): #display a bot chat message
            st.markdown(chat_response) #display bot's latest response
            with st.expander("Resources"):
                for doc in docs:
                    st.write(doc)
        
        st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history

if __name__ == "__main__":
    main()