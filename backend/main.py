from flask_cors import CORS
from flask import Flask
import flask
import httplib2
from urllib.parse import quote

import os, json, re, time
from datetime import datetime
from numpy import random

from google.cloud import storage, logging, tasks_v2
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.language_models import CodeGenerationModel
import google.auth

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from utils import task
from config import SERVICE_NAME, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, SCOPES, CHUNK_SIZE, PROVIDER, FAIL_SAFE_HTML

app = Flask(__name__)
CORS(app)

http = httplib2.Http()
headers = {"Metadata-Flavor": "Google"}
uri = 'http://metadata.google.internal/computeMetadata/v1/project/project-id'
result = http.request(uri=uri, method='GET', headers=headers)
project_id = result[1].decode()
log_name = SERVICE_NAME
res = logging.Resource(
    type="cloud_run_revision",
    labels={
        "project_id":project_id,
        "service_name":SERVICE_NAME
        }
    )


creds, project = google.auth.default(scopes=SCOPES)

# logging client
log_client = logging.Client()
logger = log_client.logger(log_name)
logger.default_resource = res

# cloud tasks client
ct_client = tasks_v2.CloudTasksClient()

# storage client
gs_client = storage.Client()
creds_bucket_name = 'c-robert-sandbox-credentials'
creds_blob_name = 'token_mistralai.json'
creds_bucket = gs_client.get_bucket(creds_bucket_name)
creds_blob = creds_bucket.get_blob(creds_blob_name)
creds_json_str = creds_blob.download_as_string().decode()
creds_json = json.loads(creds_json_str)
MISTRAL_API_KEY = creds_json['MISTRAL_API_KEY']

mistral_client = MistralClient(api_key=MISTRAL_API_KEY)

vertexai.init(project=project_id, location="us-central1", credentials=creds)
    


@app.route("/processPrompt", methods=['GET', 'POST'])
def process_prompt():
    params = dict(flask.request.args)
    data = flask.request.data.decode()
    logger.log_text('payload type %s'%type(data))
    logger.log_text(data)
    if data == '':
        logger.log_text("could not retrieve prompt from payload, defaulting to returning a joke", severity='INFO')
        data = json.dumps({"prompt" : "just write something funny, but appropriate", "response_type" : "txt"})

    data_dict = json.loads(data)
    prompt = data_dict.get('prompt')
    if prompt == '' or prompt is None:
        logger.log_text("could not retrieve prompt from payload, defaulting to returning a joke", severity='INFO')
        prompt = "just write something funny, but appropriate"

    
    provider = params.get('provider')
    if provider == '' or provider is None:
        logger.log_text(f"could not retrieve provider from payload, defaulting to {PROVIDER}", severity='INFO')
        provider = PROVIDER

    
    # evaluate whether output should be text or HTML
    model = GenerativeModel("gemini-pro")
    response_type_prompt = f"""based on the user prompt below, tell whether you think the user wants a simple text answer or expects an HTML code ? 
        {prompt}
        answer simply with 'txt' or 'html'"""
    responses = model.generate_content(response_type_prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.1,
            "top_p": 1
        },
        safety_settings=[],
    stream=True,
    )
    response_type = '\n'.join([response.text for response in responses])
    logger.log_text(f'response type {response_type}')
    
    if response_type == 'html':
        prompt = f'{prompt}\nanswer with an html code that can be directly displayed in a browser'
    logger.log_text(f'prompt \n{prompt}', severity='INFO')
    content = None
    if provider == 'gemini':
        model = GenerativeModel("gemini-1.0-pro-001")
        responses = model.generate_content(prompt,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.1,
                "top_p": 1
            },
            safety_settings=[],
        stream=True,
        )
        
        try:
            content = '\n'.join([response.text for response in responses])
        except:
            logger.log_text('ran into an error with gemini response switching to bison code', severity='INFO')
            # logger.log_text(response, severity='INFO')
            parameters = {
                "candidate_count": 1,
                "max_output_tokens": 2048,
                "temperature": 0.1
            }
            model = CodeGenerationModel.from_pretrained("code-bison")
            response = model.predict(
                prompt,
                **parameters
            )
            content = response.text
    elif provider == 'mistral':
        messages = [ChatMessage(role="user", content=prompt)]
        model = 'tiny'
        chat_response = mistral_client.chat(model=model, messages=messages)
        content = chat_response.choices[0].message.content

    logger.log_text(f'initial LLM response:\n{content}')
    
    if content is None:
        content = "something went wrong, check logs"
    elif response_type == 'html':
        re_match = re.match(r'.*?(<html>.*</html>)', content, flags=re.S)
        if re_match is not None:
            content = re_match.groups()[0]
        else:
            content = FAIL_SAFE_HTML
    logger.log_text(content)
    return {'type':response_type, 'response':content}





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))