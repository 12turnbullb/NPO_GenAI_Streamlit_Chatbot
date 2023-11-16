import streamlit as st
from langchain.llms.bedrock import Bedrock
import os
import json
import boto3
import sys
import re

bedrock = boto3.client(service_name='bedrock-runtime')


# evironment variables
# export BWB_REGION_NAME="us-east-1"
# export BWB_PROFILE_NAME="default" 
# export BWB_ENDPOINT_URL="https://bedrock.us-east-1.amazonaws.com"
# command to run the app: streamlit run main.py
#VOLTA

def clean_json(string):
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)
    #string = re.sub(r'[.+?]', '', string)
    string = re.sub(r'[+]', '', string)
    return string

def get_llm():
    
    model_kwargs =  { 
        "maxTokenCount": 4024, 
        "stopSequences": [], 
        "temperature": 0, 
        "topP": 0.9 
    }

    model_kwargs_claude = {
        "max_tokens_to_sample": 2000
    }
    
    llm = Bedrock(
        #credentials_profile_name=os.environ.get("BWB_PROFILE_NAME"), #sets the profile name to use for AWS credentials (if not the default)
        #region_name=os.environ.get("BWB_REGION_NAME"), #sets the region name (if not the default)
        client = bedrock,
        # endpoint_url=os.environ.get("BWB_ENDPOINT_URL"), #sets the endpoint URL (if necessary)
        model_id="anthropic.claude-instant-v1", #"anthropic.claude-v2", #"amazon.titan-tg1-large", #use the Anthropic Claude model
        model_kwargs=model_kwargs_claude) #configure the properties for Claude
    
    return llm

def get_text_response(user_input): #text-to-text client function
    llm = get_llm()
    
    prompt = user_input
    
    return llm.predict(prompt) #return a response to the prompt

def click_button():
    st.session_state.clicked = True
    st.session_state.cycle_questions = True
    st.session_state.disabled = False

def disable():
    st.session_state.disabled = True

def main(url_of_doc, model_used, customer_name, language):
    if 'quiz_generated' not in st.session_state:
        st.session_state['quiz_generated'] = None
        questions = []
        theQuestions = []

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    if 'cycle_questions' not in st.session_state:
        st.session_state.cycle_questions = True

    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0

    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    st.title('Quiz App - ' + customer_name)
    # Generate 20 quiz questions using Bedrock Titan
    print(st.session_state['quiz_generated'])
    if st.session_state['quiz_generated'] == None:
        print("\n\nIn getting questions.\n\n")
        questions = []
        theQuestions = []
        for i in range(20):
            #prompt = f"Human: Produce JSON of a trivia question about science with 4 potential answers listed and the correct answer listed. Produce the json only.  Assistant:"  
            #prompt = f"""Human: Produce JSON of a trivia question about science with 4 potential answers listed and the correct answer listed. Create a JSON object which has a property named "question", a property named "answer" that lists 4 potential answers, and a property named correctAnswer which has the correct answer.
            #        The resulting JSON object should be in this format: '"question":"string","answers":"list", "correctAnswer":"string"'. Produce json only. Assistant:"""
            prompt = f"""Human: Produce JSON of a detailed, role-based scenario based question about the material at these urls: """ + url_of_doc + """ with 4 potential answers listed and the correct answer listed. Create a JSON object which has a property named "question", a property named "answer" that lists 4 potential answers, and a property named correctAnswer which has the correct answer.
                    The resulting JSON object should be in this format: '"question":"string","answers":"list", "correctAnswer":"string"'. Produce json only. Assistant:"""
            response = response_content = get_text_response(user_input=prompt)
            response = response.strip('\n')
            response = response.strip("```json")
            response = response.strip("```")
            response = response.strip("`")
            response = response.strip("```json")
            response = response.strip("Here is a sample trivia question in JSON format:")
            response = response.strip("`")
            response = response.strip("json")
            response = response.strip("he JSON object of a trivia question with potential answers and the correct answer:")
            response = response.strip("4 potential answers and the correct answer listed:")
            #print (response)
            questions.append(response)
        #print(questions)
        for question in questions:
            print("\n\nThe question: " + question + "\n\n")
            question = clean_json(question)
            theQuestions.append(json.loads(question))
            #break
        print(theQuestions[0]["question"])
        st.session_state['quiz_generated'] = "generated"
        st.session_state['the_questions'] = theQuestions

    # Track current question index
    #st.session_state.question_index = -1

    # Button to cycle through questions
    
    #st.text(st.session_state['the_questions'][question_index]["question"])
    #if st.session_state.cycle_questions:
        
    with st.form("my_form"):
        #st.write("Inside the form")
        answer = st.radio(
        st.session_state['the_questions'][st.session_state.question_index]["question"],
        [st.session_state['the_questions'][st.session_state.question_index]["answers"][0], 
        st.session_state['the_questions'][st.session_state.question_index]["answers"][1], 
        st.session_state['the_questions'][st.session_state.question_index]["answers"][2],
        st.session_state['the_questions'][st.session_state.question_index]["answers"][3]])#,
        #captions = [st.session_state['the_questions'][st.session_state.question_index]["answers"][0], 
        #            st.session_state['the_questions'][st.session_state.question_index]["answers"][1],
        #            st.session_state['the_questions'][st.session_state.question_index]["answers"][2], 
        #            st.session_state['the_questions'][st.session_state.question_index]["answers"][3]])

        submitted = st.form_submit_button("Submit", on_click=disable, disabled=st.session_state.disabled)
        if submitted:
            #st.write("Selected answer: " + answer + " correct answer from json: " + st.session_state['the_questions'][st.session_state.question_index]["correctAnswer"])
            if answer == st.session_state['the_questions'][st.session_state.question_index]["correctAnswer"]:
                st.write('Correct!')
            else:
                st.write("Incorrect. The correct answer is " + st.session_state['the_questions'][st.session_state.question_index]["correctAnswer"])
            st.session_state.question_index = (st.session_state.question_index + 1) % len(st.session_state['the_questions'])
            #st.session_state.question_index = st.session_state.question_index + 1
            print("\n\nIn Next Question. Index = " + str(st.session_state.question_index) + "\n\n")
            st.session_state.cycle_questions = False
        #agree = st.checkbox('I agree')

        #if agree:
        #    st.write('Great!')
    #with st.form("my_other_form"):
    #    st.write("Inside the form")
    #    slider_val = st.slider("Form slider")
    #    checkbox_val = st.checkbox("Form checkbox")
    #    answer = st.radio(
    #    st.session_state['the_questions'][st.session_state.question_index]["question"],
    #    [st.session_state['the_questions'][st.session_state.question_index]["answers"][0]])

        # Every form must have a submit button.
    #    submitted = st.form_submit_button("Submit")
    #    if submitted:
    #        st.write("slider", slider_val, "checkbox", checkbox_val)

    #st.write("Outside the form")
    st.button('Next Question', on_click=click_button)

if __name__ == "__main__":
    # url of doc can be a comma separated list of pdf doc urls, no quotes needed
    # here's an example run command: 
    # streamlit run main.py https://www.pallakkindt.com/images/service/7.2_Radiaographic_Testing_Procedure.pdf,https://www.pallakkindt.com/images/service/Magnetic-Particle-Testing-Procedure.pdf ASNT Claude
    url_of_doc = sys.argv[1]
    customer_name = sys.argv[2]
    model_used = sys.argv[3]
    lanuage = 'en'
    print('url_of_doc: ' + str(url_of_doc))
    main(url_of_doc, model_used, customer_name, lanuage)