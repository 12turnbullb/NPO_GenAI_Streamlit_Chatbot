# 5_Bedrock_agent

Chat application that makes an API call to a Bedrock agent configured via the AWS console. This agent has been configured to make calls to a DynamoDB table to retrieve member IDs and update member email addresses.

## Running the lab

To get started, follow these steps:

1. **Open a Cloud9 terminal:**
   Window > New Terminal

2. **Navigate to the lab folder**:

   ```bash
   cd 5_Bedrock_agent/
   ```

3. **Create an Amazon Bedrock Agent:** You will need to first configurate an agent in the Amazon Bedrock console. This requires setting up an OpenAPI schema, and a lambda function to make API calls. Visit [this link](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) to learn more about setting up an agent.

4. **Update the code to point to your agent:** Update the streamlit files call_agent() function to refer to your specific agent ID and alias.

5. **Run the agent application:** The run command accepts two additonal parameters 1) a comma separated list of PDF document URLS and 2) a customer name.

   ```bash
   streamlit run 1_agent_streamlit_app.py --server.port 8080
   ```

6. **Preview the running application:** Click on 'Preview' in the top menu then select 'Preview running application' to open a browser window that loads the Streamlit application.

## Script Descriptions

1. **1_agent_streamlit_app.py:**
   This script generates a standard chat interface where all input is fed to a Bedrock agent via API call. The responses are parsed and sent back to the user. The trace results are also collected for context to the agent's thinking process.

2. **2_agent_login_streamlit_app.py:**
   This script takes the agent a step further by generating a pseudo-login screen that passes the email entered into the username as a promptSessionAttribute to the Agent itself. The Agent orchestration prompt will need to be updated to include the promptSessionAttribute values.
