# NPO Generative AI with Amazon Bedrock

Welcome to the **NPO Generative AI with Amazon Bedrock** repository! This collection of Python scripts serves as a guide to help you understand and implement generative artificial intelligence (AI) using Amazon Bedrock. Each script focuses on different aspects of generative AI paired with an easy-to-use front end package called [Streamlit](https://streamlit.io/) to create a chatbot UI.

## Getting Started

To get started, follow these steps:

1. **Set up a Cloud9 development environment**
   Follow the instructions on [this workshop page](https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/prerequisites/cloud9-setup) to setup an AWS Cloud9 integrated development environment. This ensures all users are starting from the same base machine and helps avoid dependency issues.

   **Note:** If the Cloud9 instance isn't available, you may need to try a different region e.g. us-west-2.

2. **Open a Cloud9 terminal:**
   Window > New Terminal

3. **Clone the repository:**
   ```bash
   git clone https://github.com/12turnbullb/NPO_GenAI_Streamlit_Chatbot.git
   ```
4. **Navigate to the lab directory:**

   ```bash
   cd NPO_GenAI_Streamlit_Chatbot
   ```

5. **install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
6. **Amazon Bedrock Access:**
   Ensure the region that you've created your Cloud9 instance has access to Amazon Bedrock.

   - Navigate to the Amazon Bedrock console
   - Choose **Model Access** from the left menu
   - Select **Manage model access**
   - In this lab we are using the Claude model from Anthropic, and the Jurassic models from AI21 Labs. Check the Anthropic and AI21 Labs models and scroll down to select **Save changes**

7. **Test Bedrock Access:** Run the 0_bedrock_test.py script in the terminal to test that your evironment has access to call the Bedrock APIs. Be sure you're in the home directory NPO_GenAI_Streamlit_Chatbot.

   ```bash
   python 0_bedrock_test.py
   ```

   The script passes a prompt asking Claude and Jurassic to explain a black hole to 8th graders and returns the responses. You can compare the outputs of the two different models in the terminal.

8. **Navigate to a lab:** Follow the README.md within each lab to execute the scripts.

   ```bash
   # Example
   cd 0_Chatbot_simple/
   ```

## Lab Descriptions

1. **0_Chatbot_simple:**
   Introductory for open LLM question and answer. One script contains a simple prompt submission and LLM response, and another script includes memory to create a conversational chain.

2. **1_Chatbot_simple_RAG:**
   LLM with RAG for question and answer. Ingest PDF data to a local vector store, then pass as context for question answering. No memory, just a simple prompt submission and a customer-data specific response.

3. **2_Chatbot_memory_RAG:**
   LLM with RAG and memory for linked question and answer. Ingest PDF data to local vector store, then pass as context to the conversational chain.

4. **2a_Chatbot_memory_RAG_realtime:**
   LLM with RAG and memory for linked question and answer. Instead of saving PDFs to a local vector store, this version indexes the data in-memory in realtime as you load the page. It does not persist the vector store locally, each page reload kicks off the indexing process.

5. **3_Chatbot_kendra_RAG:**
   LLM with RAG for question and answer. Instead of ingesting customer data to a local vector store, connect to an Amazon Kendra index that has been populated ahead of time. Kendra can connect to Amazon S3 buckets, crawl websites and more to build a corpus of data.

6. **4_Chatbot_quiz:**
   Quiz generator that passes in URLs as context to develop a question bank then leads users through a custom quiz on Streamlit.

7. **5_Bedrock_agent:**
   Chat application that makes an API call to a Bedrock agent configured via the AWS console. This agent has been configured to make calls to a DynamoDB table to retrieve member IDs and update member email addresses.

## Additional Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html): Explore the official documentation for Amazon Bedrock.
- [AWS Blog - Generative AI](https://aws.amazon.com/blogs/machine-learning/category/artificial-intelligence/generative-ai/): Stay updated with the latest insights and use cases related to generative AI on AWS.
