import streamlit as st #all streamlit commands will be available through the "st" alias
import agent_chatbot_lib as glib #reference to local lib script
import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime')
agent_client = boto3.client(service_name='bedrock-agent-runtime')

def call_agent(prompt, session):

    response = agent_client.invoke_agent(
    sessionState={
        # 'sessionAttributes': {
        #     'string': 'string'
        # },
        # # Use these attributes to pass data into the orchestration prompt of the agent
        #'promptSessionAttributes': {
        #    'memberEmail': email
        #}
    },
    agentId='MVU6VWIWET',
    agentAliasId='OOXVG6QGNA',
    sessionId=session,
    endSession=False,
    enableTrace=True,  
    inputText= prompt
    )

    event_stream = response['completion']

    result_dict = {}

    for event in event_stream:

        if 'chunk' in event:
            data = event['chunk']['bytes']
            answer = data.decode("utf-8")
            result_dict["chunk"] = answer
        elif 'trace' in event:
            trace = event['trace']['trace']
            #print('-------------------------------------------------------')
            #print(trace)
            #print('-------------------------------------------------------')
            if "orchestrationTrace" in trace:
                orchestration = event['trace']['trace']['orchestrationTrace']
                if "rationale" in orchestration:
                    trace = json.dumps(event['trace']['trace']['orchestrationTrace']['rationale']['text'], indent=2)
                    result_dict["trace"] = trace

    return result_dict

def navigate_to_bedrock_agent():

    st.title("Amazon Bedrock Chatbot") #page title
    st.caption("Welcome! Ask this bot to perform functions like retrieving your member ID or updating your email address. Ensure your current email address exists in the profile database.")
    
    # Create a session ID to associate with this chat to hold the conversation history in memory
    # The memory will expire for this session after 30 minutes
    session = st.text_input("Session:")

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
        
        with st.chat_message("user"): #display a user chat message
            st.markdown(input_text) #renders the user's latest message
        
        st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history

        dict_raw = call_agent(input_text, session)

        chat_response = dict_raw["chunk"]
        latest_trace = dict_raw["trace"]

        with st.chat_message("assistant"): #display a bot chat message
            st.markdown(chat_response) #display bot's latest response
            with st.expander("Latest trace results"):
                if latest_trace == '""': 
                    st.markdown("No rationale included.")
                else:
                    st.markdown(latest_trace)

        st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history


if __name__ == "__main__":
    navigate_to_bedrock_agent()
