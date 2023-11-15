import json
import boto3
import streamlit as st
import anthropic
import os
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
import time
from tempfile import gettempdir
import ai21
import re

#session = Session(profile_name="AdministratorAccess-904262394592")
#polly = session.client("polly") 

#key = os.environ['AWS_ACCESS_KEY_ID']
#secret = os.environ['AWS_SECRET_ACCESS_KEY']
#region = os.environ['AWS_DEFAULT_REGION']
region = "us-east-1"
#ai21.api_key = os.environ.get('AI21_API_KEY')


polly = boto3.Session(region_name='us-east-1').client('polly')

translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
original_text = ''
image_name = 'Misti-A Memory'

if 'img_summary' not in st.session_state:
    st.session_state['img_summary'] = None
if 'image_insights' not in st.session_state:
    st.session_state['image_insights'] = None
if 'original_text' not in st.session_state:
    st.session_state['original_text'] = None

s3 = boto3.client('s3',region_name='us-east-1')
comprehend = boto3.client('comprehend',region_name='us-east-1')
rekognition = boto3.client('rekognition',region_name='us-east-1')
#languages = ['English', 'Spanish', 'German', 'Portugese', 'Irish', 'Korean', 'Star Trek - Klingon', 'Star Trek - Ferengi', 'Italian', 'French', 'Japanese', 'Mandarin', 'Tamil', 'Hindi', 'Telugu', 'Kannada', 'Arabic', 'Hebrew']
languages = ['English', 'Spanish', 'Hindi', 'Chinese', 'German', 'Portugese', 'Dutch', 'Italian', 'French']
# Get environment variables
# ant_api_key = os.environ['ant_api_key']
# bucket = os.environ['bucket']
# im_endpoint_name = os.environ['im_endpoint_name']
# tx_endpoint_name = os.environ['tx_endpoint_name']
#br_endpoint_name = os.environ['fsi_index_id']
# ant_name = os.environ['ant_name']

#bedrock = boto3.client('bedrock',region_name=region)
bedrock = boto3.client(service_name='bedrock-runtime')

st.set_page_config(page_title="GenAI Image Analyzer", page_icon="flashlight")

st.markdown(
    """
    ### :red[Note] 
    - For showcasing at large events please reach out to rangarap@ or dabounds@ for inputs
    - Please review and comply with the [Generative AI Acceptable Use Policy](https://policy.a2z.com/docs/568686/publication)
    - Use these selection of [samples for playing with the demos](https://amazon.awsapps.com/workdocs/index.html#/folder/085a7d2cc912f998468435fdf7eab6e9bb09ae855acfb9b16aea59de7d547e21).  
    - The demos should not be considered as an actual prototype or working version of a proposed solution
    - Source code available in the [GitLab repo](https://gitlab.aws.dev/dabounds/gen-ai-demos) and associated [Documentation](https://gitlab.aws.dev/dabounds/gen-ai-demos/-/tree/development/static/Documentation).
    """)

st.markdown("# Derive insights from images")
st.sidebar.header("GenAI Image Analyzer")


model = 'Anthropic Claude'
#model = 'Titan Large'
#model = 'Jurassic'
#argument = int(sys.argv[1])
#if argument == 1:
#    pic_name = "Misti - A Memory"


def call_anthropic(prompt_text, max_tokens_to_sample=1024, temperature=0.7, top_k=250, top_p=1):
    model_id = "anthropic.claude-v2"
    body = {
        "prompt": anthropic.HUMAN_PROMPT+prompt_text+anthropic.AI_PROMPT,
        "max_tokens_to_sample": max_tokens_to_sample
    }
    body_string = json.dumps(body)
    body = bytes(body_string, 'utf-8')
    response = bedrock.invoke_model(
        modelId = model_id,
        contentType = "application/json",
        accept = "application/json",
        body = body)
    response_lines = response['body'].readlines()
    json_str = response_lines[0].decode('utf-8')
    json_obj = json.loads(json_str)
    return json_obj['completion']

def call_ai21(prompt):
    response = ai21.Completion.execute(
    model='j1-large',
    prompt=prompt,
    temperature=0.65,
    minTokens=4,
    maxTokens=32,
    numResults=1,
    topKReturn=0,
    topP=1,
    stopSequences=["##"]
    )
    #response_body = response
    #print("jurassic response: " + str(response_body))
    multilingual_response = {str(response['completions'][0]['data']['text'])}
    #string_response = str(multilingual_response)
    #print(string_response + '\n')
    #string_response.replace("{","")
    #string_response.replace("}","")
    #string_response.replace("\n","")
    return multilingual_response

def call_titan(prompt_text, max_tokens_to_sample=1024, temperature=0.9, top_k=250, top_p=1):
    model_id = "amazon.titan-tg1-large" 
    prompt_config = {
        "inputText": prompt_text,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": temperature, #0.5,
            "topP": top_p, #0.2,
        },
    }
    body = json.dumps(prompt_config)
    
    print("body string: " + body + "\nend of body string")
    
    model_id = "amazon.titan-tg1-large"  
    accept = "application/json"
    contentType = "application/json"
    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    results = response_body.get("results")[0].get("outputText")
    return results

def GetAnswers(summary, query):

    if query == "cancel":
        answer = 'It was swell chatting with you. Goodbye for now'
    
    #elif sentiment == 'NEGATIVE':
    #    answer = 'I do not answer questions that are negatively worded or that concern me at this time. Kindly rephrase your question and try again.'

            
    else:
        generated_text = ''
        if model.lower() == 'anthropic claude':  
            generated_text = call_anthropic(summary+'. Answer from this summary, considering the art work, in '+language+': '+ query.strip("query:"))
            if generated_text != '':
                answer = str(generated_text)+' '
            else:
                answer = 'Claude did not find an answer to your question, please try again'   
        elif model.lower() == 'titan large':
            generated_text = call_titan(summary+'. Answer from this summary, considering the art work, in '+language+': '+ query.strip("query:"))
            st.session_state['original_text'] = generated_text
            if language == 'Spanish':
                result = translate.translate_text(Text=generated_text, 
                    SourceLanguageCode="en", TargetLanguageCode="es")
                generated_text = result.get('TranslatedText')
            elif language == 'Chinese':
                result = translate.translate_text(Text=generated_text, 
                    SourceLanguageCode="en", TargetLanguageCode="zh")
                generated_text = result.get('TranslatedText')
            elif language == 'Hindi':
                result = translate.translate_text(Text=generated_text, 
                    SourceLanguageCode="en", TargetLanguageCode="hi")
                generated_text = result.get('TranslatedText')
            if generated_text != '':
                answer = str(generated_text)+' '
            else:
                answer = 'Titan did not find an answer to your question, please try again'
        elif model.lower() == 'jurassic':
            if language == 'Spanish':
                multilingual_prompt = summary+'. Respuesta de este resumen, considerando el arte abstracto, en '+language+': '+ query.strip("query:")
            elif language == 'English':
                multilingual_prompt = summary+'. Answer from this summary, considering the art work, in '+language+': '+ query.strip("query:") 
            #generated_text = call_ai21(summary+'. Answer from this summary, considering the art work, in '+language+': '+ query.strip("query:"))
            titan_text = call_titan(multilingual_prompt)
            generated_text = call_ai21(titan_text)
            if generated_text != '':
                answer = str(generated_text)+' '
            else:
                answer = 'Jurassic did not find an answer to your question, please try again'
    return answer          

#speak response
def speak_response(text, language):
    speaker = 'Joanna'
    if language == 'en-US':
        speaker = 'Joanna'
    elif language == 'es-MX':
        speaker = 'Mia'
    elif language == 'cmn-CN':
        speaker = 'Zhiyu'
    elif language == 'hi-IN':
        speaker = 'Aditi'
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                        VoiceId=speaker, LanguageCode = language)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)
    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
           output = os.path.join(gettempdir(), "speech.mp3")
           try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                   #speech_file = file
                   file.write(stream.read())
           except IOError as error:
               # Could not write to file, exit gracefully
               print(error)
               sys.exit(-1)
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)
    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])
    #print('\n' + speech_file.name + '\n')
    #speech_file.close()
    #os.remove(file.name)

#upload audio file to S3 bucket
def upload_image_detect_labels(bytes_data):
    min_confidence=95
    custom_model = 'arn:aws:rekognition:us-east-1:904262394592:project/Georgia-OKeeffe/version/Georgia-OKeeffe.2023-08-25T15.05.08/1692990308087'
    summary = ''
    label_text = ''
    st.session_state['image_insights'] = None
    response = rekognition.detect_labels(
        Image={'Bytes': bytes_data},
        Features=['GENERAL_LABELS']
    )
    #response = rekognition.detect_custom_labels(Image={'Bytes': bytes_data},
    #    MinConfidence=min_confidence,
    #    ProjectVersionArn=custom_model)
    text_res = rekognition.detect_text(
        Image={'Bytes': bytes_data}
    )

    celeb_res = rekognition.recognize_celebrities(
        Image={'Bytes': bytes_data}
    )


    for celeb in celeb_res['CelebrityFaces']:
        label_text += celeb['Name'] + ' ' 

    for text in text_res['TextDetections']:
        if text['Confidence'] > 90:
            label_text += text['DetectedText'] + ' '

    for label in response['Labels']: # CustomLabels
        if label['Confidence'] > 90:
            label_text += label['Name'] + ' '

    if model.lower() == 'anthropic claude':  
        generated_text = call_anthropic("Summarize the image, considering the art work by Georgia O'Keeffe, in "+language+" without any hallucinations in 200 words strictly adhering to what is mentioned in the labels only: "+ label_text)
        if generated_text != '':
            generated_text.replace("$","USD")
            summary = str(generated_text)+' '
        else:
            summary = 'Claude did not find an answer to your question, please try again'    
        return summary  
    elif model.lower() == 'titan large':  
        generated_text = call_titan("Describe the image '" + image_name + "' in "+language+" using these labels: "+ label_text + " to give context.")
        st.session_state['original_text'] = generated_text
        #print("generated text before translation: ", st.session_state['original_text'], "\n")
        if language == 'Spanish':
            result = translate.translate_text(Text=generated_text, 
                SourceLanguageCode="en", TargetLanguageCode="es")
            generated_text = result.get('TranslatedText')
        elif language == 'Chinese':
            result = translate.translate_text(Text=generated_text, 
                SourceLanguageCode="en", TargetLanguageCode="zh")
            generated_text = result.get('TranslatedText')
        elif language == 'Hindi':
                result = translate.translate_text(Text=generated_text, 
                    SourceLanguageCode="en", TargetLanguageCode="hi")
                generated_text = result.get('TranslatedText')
        if generated_text != '':
            generated_text.replace("$","USD")
            summary = str(generated_text)+' '
        else:
            summary = 'Titan did not find an answer to your question, please try again'    
        #print("generated text after translation: ", st.session_state['original_text'], "\n")
        return summary
    elif model.lower() == 'jurassic':  
        generated_text = call_ai21('Summarize the image, considering the art work, in '+language+' without any hallucinations in 200 words strictly adhering to what is mentioned in the labels only: '+ label_text)
        if generated_text != '':
            #generated_text.replace("$","USD")
            summary = str(generated_text)+' '
        else:
            summary = 'Jurassic did not find an answer to your question, please try again'    
        return summary


st.write("**Instructions:** \n - Browse and select your image file. You can [download these samples](https://amazon.awsapps.com/workdocs/index.html#/folder/8a926bdf7852d8c940d4238017b48678d6fcfadaaa918d03a7965db6822041f6) or use your own \n - You will see a summary based on labels identifed by Amazon Rekognition \n - Type your query in the search bar to get image insights")

c1, c2 = st.columns(2)
c1.subheader("Upload your image file")
uploaded_img = c1.file_uploader("**Select an image file**", type=['jpg','jpeg','png'])
#if st.session_state.image_insights is not None:
try:
    image_name = os.path.splitext(uploaded_img.name)[0]
    print("image name: ", image_name, "\n")
except:
    image_name = ''
default_lang_ix = languages.index('English')
c2.subheader("Select an spoken language")
language = c2.selectbox(
    'Only Alpha and Beta quadrant languages supported at this time. For new requests, please contact C-3PO',
    options=languages, index=default_lang_ix)
img_summary = ''
p_summary = ''
if uploaded_img is not None:
    if 'jpg' in uploaded_img.name or 'png' in uploaded_img.name or 'jpeg' in uploaded_img.name:        
        c1.success(uploaded_img.name + ' is ready for upload')
        if c1.button('Upload'):
            with st.spinner('Uploading image file and starting Amazon Rekognition label detection...'):
                inapp_res = rekognition.detect_moderation_labels(Image={'Bytes': uploaded_img.getvalue()})
                if len(inapp_res['ModerationLabels']) == 0:
                    img_summary = upload_image_detect_labels(uploaded_img.getvalue())
                    #img_summary = re.escape(img_summary).replace("\","")
                    img_summary = img_summary.replace("$","\$")
                else:
                    st.write("Inappropriate content detected in image. Please change your image and try again")
    else:
        st.write('Incorrect file type provided. Please select either a JPG or PNG file to proceed')
    # Check job status
    

if len(img_summary) >= 5:
    st.session_state['img_summary'] = img_summary

if st.session_state.img_summary:
    if uploaded_img is not None:
        st.image(uploaded_img)
    st.markdown('**Image summary**: \n')

    st.write(str(st.session_state['img_summary']))
    lang = 'en-US'
    if language == 'Spanish':
        lang = 'es-MX'
    elif language == 'Chinese':
        lang = 'cmn-CN'
    elif language == 'Hindi':
        lang = 'hi-IN'
    if st.session_state.image_insights is None:
        speak_response(str(st.session_state['img_summary']), lang)
        st.session_state.image_insights = 'some'
    
    # don't do the 3 summary prompts
    if model.lower() == 'anthropic claude':  
        p_text = call_anthropic('Generate three prompts to query the summary: '+ st.session_state.img_summary)
        p_text1 = []
        p_text2 = ''
        if p_text != '':
            p_text.replace("$","USD")
            p_text1 = p_text.split('\n')
            #p_text1 = re.split('(?<=\D)(?=\d)', p_text)
            for i,t in enumerate(p_text1):
                if i > 1:
                    p_text2 += t.split('\n')[0]+'\n\n'
            p_summary = p_text2
    elif model.lower() == 'titan large':
        print("\ngenerating three prompts\n")
        #p_text = call_titan('Generate three prompts to query the summary: '+ st.session_state.img_summary)
        p_text = call_titan('Generate three prompts to query the summary: '+ st.session_state['original_text'])
        if language == 'Spanish':
            result = translate.translate_text(Text=p_text, 
                SourceLanguageCode="en", TargetLanguageCode="es")
            p_text = result.get('TranslatedText')
        elif language == 'Chinese':
            result = translate.translate_text(Text=p_text, 
                SourceLanguageCode="en", TargetLanguageCode="zh")
            p_text = result.get('TranslatedText')
        elif language == 'Hindi':
            result = translate.translate_text(Text=p_text, 
                SourceLanguageCode="en", TargetLanguageCode="hi")
            p_text = result.get('TranslatedText')
        #p_text.replace("?","?\n")
        print("\nsuggested prompts generated\n" + p_text + "\n")
        p_text1 = []
        p_text2 = ''
        if p_text != '':
            #p_text.replace("$","USD")
            #p_text1 = p_text.split('\n')
            #for i,t in enumerate(p_text1):
            #    if i > 1:
            #        p_text2 += t.split('\n')[0]+'\n\n'
            #    else:
            #        p_text2 = p_text
            #p_summary = p_text2
            strlist = re.split('(?<=\D)(?=\d)', p_text)
            for item in strlist:
                p_summary = p_summary + item + '\n'

    st.sidebar.markdown('### Suggested prompts for further insights \n\n' + 
                p_summary)
    
    input_text = st.text_input('**What insights would you like?**', key='text')
    if input_text != '':
        if st.session_state.image_insights is not None:
            #result = GetAnswers(st.session_state.img_summary,input_text)
            # need to translate input_text to english before calling GetAnswers
            # also need to store original_text in session
            if language == 'Spanish':
                result = translate.translate_text(Text=input_text, 
                    SourceLanguageCode="es", TargetLanguageCode="en")
            result = GetAnswers(st.session_state['original_text'],input_text)
            result = result.replace("$","\$")
            st.write(result)
            if language == 'Spanish':
                lang = 'es-MX'
            elif language == 'Chinese':
                lang = 'cmn-CN'
            elif language == 'Chinese':
                lang = 'hi-IN'
            speak_response(result, lang)
        





