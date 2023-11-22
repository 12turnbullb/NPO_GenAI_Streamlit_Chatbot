# 2a_Chatbot_memory_RAG_realtime

LLM with RAG and memory for linked question and answer. Instead of saving PDFs to a local vector store, this version indexes the data in-memory in realtime as you load the page. It does not persist the vector store locally, each page reload kicks off the indexing process.

## Running the lab

To get started, follow these steps:

1. **Open a Cloud9 terminal:**
   Window > New Terminal

2. **Navigate to the lab folder**:

   ```bash
   cd 2a_Chatbot_memory_RAG_realtime
   ```

3. **Populate the 'data' folder with custom data:** Empty the 'data' folder and add a few PDFs that are specific to your use case.

   **Note:** To avoid long runtimes, keep this dataset small as the application will recreate an in-memory vector store on each page load.

4. **Run the RAG Q&A with memory:**
   ```bash
   streamlit run 1_rag_streamlit_app.py --server.port 8080
   ```
5. **Preview the running application:** Click on 'Preview' in the top menu then select 'Preview running application' to open a browser window that loads the Streamlit application.

## Script Descriptions

1. **1_rag_streamlit_app.py:**
   Script will index your local documents to an in-memory vector store first, then run FAISS (Facebook AI Similarity Search) to pull relevant document chunks and return them as context to the user prompt. Conversation memory is retreived for context and stored for history. User submits a query, function adds in the relevant context from our in-memory vector store, and sends the prompt to Bedrock. The results are output to the UI frame by Streamlit.

2. **rag_chatbot_lib.py:**
   Script to build the conversation chain and memory structure to support the contextual chat. This script also generates the in-memory index using the PDFs in our local 'data' directory. This script is referenced by the 1_rag_streamlit_app.py script.
