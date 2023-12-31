# 1_Chatbot_simple_RAG

LLM with RAG for question and answer. Ingest PDF data to a local vector store, then pass as context for question answering. No memory, just a simple prompt submission and a customer-data specific response.

## Running the lab

To get started, follow these steps:

1. **Open a Cloud9 terminal:**
   Window > New Terminal

2. **Navigate to the lab folder**:

   ```bash
   cd 1_Chatbot_simple_RAG/
   ```

3. **Populate the 'data' folder with custom data:** Empty the 'data' folder and add a few PDFs that are specific to your use case.

4. **Ingest custom data to local index:** Run the 1_bedrock_pdf_ingest.py script to loop through the PDFs and create a local index of data for your LLM to use later on. This might take a few minutes, depending on how many PDFs you've included.

   ```bash
   python 1_bedrock_pdf_ingest.py
   ```

5. **Run the RAG Q&A without memory:**
   ```bash
   streamlit run 2_bedrock_streamlit.py --server.port 8080
   ```
6. **Preview the running application:** Click on 'Preview' in the top menu then select 'Preview running application' to open a browser window that loads the Streamlit application.

## Script Descriptions

1. **1_bedrock_pdf_ingest.py:**
   Simple function that takes in PDF documents from the 'data' folder, splits them into smaller chunks of text, converts the text to vectors with the Bedrock embeddings model, and stores the data in local vector store named 'local_index_test'.

2. **2_bedrock_streamlit.py:**
   Function that runs a FAISS (Facebook AI Similarity Search) to pull relevant document chunks from our local vector store and return them as context to the prompt. User submits a query, function adds in the relevant context from our local vector store, and sends the prompt to Bedrock. The results are output to the UI frame by Streamlit.
