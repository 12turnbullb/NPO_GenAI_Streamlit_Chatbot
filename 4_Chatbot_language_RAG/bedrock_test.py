
import boto3
import json
bedrock = boto3.client(service_name='bedrock-runtime')


def call_claude(prompt):

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 300,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    # text
    print('################# CLAUDE ##############')
    print('PROMPT:\n', prompt, '\n')
    print('RESPONSE:\n', response_body.get('completion'), '\n') 

    return response_body.get('completion')

def call_jurassic(prompt):

    body = json.dumps({
        "prompt": prompt,
        "maxTokens": 200
    })

    modelId = 'ai21.j2-mid'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get("body").read())

    # text
    print('################# JURASSIC ##############')
    print('PROMPT:\n', prompt, '\n')
    print('RESPONSE:', response_body.get("completions")[0].get("data").get("text"), '\n'),
    return response_body.get("completions")[0].get("data").get("text")

def main() -> None:

    claude_prompt = """Human: Explain a black hole to 8th graders in less than 20 words. Assistant:"""
    jurassic_prompt = """Explain a black hole to 8th graders in less than 20 words"""

    call_claude(claude_prompt)
    call_jurassic(jurassic_prompt)


if __name__ == "__main__":
    main()