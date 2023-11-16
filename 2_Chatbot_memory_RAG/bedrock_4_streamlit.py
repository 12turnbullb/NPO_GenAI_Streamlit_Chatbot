import json
import sys
import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
#from transformers import Tool
import streamlit as st
import bedrock_3_chatbot_lib as glib #reference to local lib script
from bedrock_2_tool import AWSGenAITool;

# need to install the anthropic library
# pip install anthropic

well_arch_tool = AWSGenAITool()

bedrock = boto3.client(service_name='bedrock-runtime')

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
        answer = well_arch_tool(input_text)
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

# why do we need translation? if you ask a question in spanish without sending to jurassic, the answer will also be in spanish, even if the RAG documents are in english. 
