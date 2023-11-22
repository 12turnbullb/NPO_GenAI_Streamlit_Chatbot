# 3_Chatbot_kendra_RAG

LLM with RAG for question and answer. Instead of ingesting customer data to a local vector store, connect to an Amazon Kendra index that has been populated ahead of time. Kendra can connect to Amazon S3 buckets, crawl websites and more to build a corpus of data.

## Running the lab

To get started, follow these steps:

1. **Open a Cloud9 terminal:**
   Window > New Terminal

2. **Navigate to the lab folder**:

   ```bash
   cd 3_Chatbot_kendra_RAG
   ```

3. **Point to your Amazon Kendra index**: Build a Kendra index populated with objects from S3, web crawlers and more. Copy the ID of your kendra index and paste it into the bedrock_RAG_with_kendra.py script near the top.

   Learn how to [create a Kendra index](https://docs.aws.amazon.com/kendra/latest/dg/create-index.html) and [connect an Amazon S3 bucket](https://docs.aws.amazon.com/kendra/latest/dg/data-source-s3.html#data-source-procedure-s3) to the index.

4. **Run the RAG Q&A without memory:**

   ```bash
   streamlit run bedrock_RAG_with_kendra.py --server.port 8080
   ```

5. **Preview the running application:** Click on 'Preview' in the top menu then select 'Preview running application' to open a browser window that loads the Streamlit application.

## Script Descriptions

1. **bedrock_RAG_with_kendra.py:**
   Function creates a chain using the Kendra index as our vector store. Builds a prompt that queries relevant documents from our Kendra index and returns it as context to our prompt. Prompt is submitted to Bedrock and the results are displayed in the UI with Streamlit.
