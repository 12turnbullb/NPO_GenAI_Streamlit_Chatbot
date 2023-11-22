# 4_Chatbot_quiz

Quiz generator that passes in URLs as context to develop a question bank then leads users through a custom quiz on Streamlit.

## Running the lab

To get started, follow these steps:

1. **Open a Cloud9 terminal:**
   Window > New Terminal

2. **Navigate to the lab folder**:

   ```bash
   cd 4_Chatbot_quiz/
   ```

3. **Collect links to to build your quiz:** The script will accept PDF URLs as parameters to build the quiz content. Collect a few PDF URLs before running the script.

4. **Run the quiz generator:** The run command accepts two additonal parameters 1) a comma separated list of PDF document URLS and 2) a customer name.

   ```bash
   streamlit run quiz_generator_streamlit.py [insert resource URLS] [insert customer name] --server.port 8080
   ```

   Example:

   ```bash
   streamlit run quiz_generator_streamlit.py https://www.pallakkindt.com/images/service/7.2_Radiaographic_Testing_Procedure.pdf,https://www.pallakkindt.com/images/service/Magnetic-Particle-Testing-Procedure.pdf ASNT --server.port 8080
   ```

5. **Preview the running application:** Click on 'Preview' in the top menu then select 'Preview running application' to open a browser window that loads the Streamlit application.

## Script Descriptions

1. **quiz_generator_streamlit.py:**
   Pass the URLs from the run command to a prompt that asks Claude to generate a multiple choice quiz using contents from the document. Streamlit parses the response into a quiz UI.
