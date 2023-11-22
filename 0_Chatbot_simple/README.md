# 0_Chatbot_simple

Introductory scripts for open LLM question and answer. One script contains a simple prompt submission and LLM response, and another script includes memory to create a conversational chain.

## Running the lab

To get started, follow these steps:

1. **Open a Cloud9 terminal:**
   Window > New Terminal

2. **Navigate to the lab folder**:

   ```bash
   cd 1_Chatbot_simple_RAG
   ```

3. **Run the Q&A WITHOUT memory script:**
   ```bash
   streamlit run 1_bedrock_streamlit.py --server.port 8080
   ```
4. **Preview the running application:** Click on 'Preview' in the top menu then select 'Preview running application' to open a browser window that loads the Streamlit application.

5. **Run the Q&A WITH memory script:**

   ```bash
   streamlit run 2_bedrock_memory_streamlit.py --server.port 8080
   ```

6. **Preview the running application:** Click on 'Preview' in the top menu then select 'Preview running application' to open a browser window that loads the Streamlit application.

## Script Descriptions

1. **1_bedrock_streamlit.py:**
   Simple function to invoke the Bedrock API. A Streamlit section to pass in the user prompt and return the LLM results to the UI frame.

2. **2_bedrock_memory_streamlit.py:**
   Simple function to invoke the Bedrock API. Memory handling to loop through chat history, and add new chats to the memory. Supported by the bedrock_memory_lib.py script.

3. **bedrock_memory_lib.py**
   Script to build the conversation chain and memory structure to support the contextual chat. Referenced by the 2_bedrock_memory_streamlit.py script.
