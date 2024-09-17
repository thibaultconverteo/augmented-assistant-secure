from flask_cors import CORS
from flask import Flask
import flask
import httplib2
from urllib.parse import quote

import os, json, re, time, uuid
from datetime import datetime
from numpy import random

from google.cloud import storage, logging, tasks_v2
# import vertexai
# from vertexai.preview.generative_models import GenerativeModel, Part
# from vertexai.language_models import CodeGenerationModel
import google.auth

# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage

from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.cloud.dialogflowcx_v3beta1 import types

from utils import task
from config import SERVICE_NAME, LOCATION, PROVIDER, FAIL_SAFE_HTML, SCOPES, LOGS_BUCKET_NAME, LOGS_BLOB_PREFIX, AGENT_ID
from config import NO_DATA_HTML

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



@app.route("/processPrompt", methods=['GET', 'POST'])
def process_prompt():
    
    
    params = dict(flask.request.args)
    logger.log_text(f'request params {json.dumps(params)}')
    
    headers_dict = dict(flask.request.headers)
    logger.log_text(f'request headers {json.dumps(headers_dict)}')
    
    session_id = headers_dict.get('Sessionid')
    if session_id == '' or session_id is None:
        logger.log_text(f"could not retrieve session id from header, intializating one", severity='INFO')
        session_id = uuid.uuid4()
    logger.log_text(f"session id {session_id}", severity='INFO')


    # session_id = params.get('sessionId')
    # logger.log_text(f"retrieved session id {session_id} from payload", severity='INFO')
    
    agent_id_key = 'Agentid'
    if agent_id_key in headers_dict:
        agent_id = headers_dict[agent_id_key]
    else:
        agent_id = AGENT_ID
    
    logger.log_text(f'session id {session_id} agent id {agent_id}')

    

    data = flask.request.data.decode()
    logger.log_text(f'session id {session_id} payload\n{data}')
    if data == '':
        logger.log_text("session id {session_id} could not retrieve prompt from payload, defaulting to returning a joke", severity='INFO')
        data = json.dumps({"prompt" : "just write something funny, but appropriate", "response_type" : "txt"})

    data_dict = json.loads(data)
    prompt = data_dict.get('prompt')
    if prompt == '' or prompt is None:
        logger.log_text("session id {session_id} could not retrieve prompt from payload, defaulting to returning a joke", severity='INFO')
        prompt = "just write something funny, but appropriate"

    
    

    if LOCATION != 'global':
        api_endpoint = f"{LOCATION}-dialogflow.googleapis.com"
    else:
        api_endpoint = "dialogflow.googleapis.com"
    client_options = {"api_endpoint": api_endpoint}

    session_client = dialogflow.SessionsClient(credentials=creds, client_options=client_options)
    
    session_path = session_client.session_path(project_id, LOCATION, agent_id, session_id)

    language_code = 'en'
    text_input = types.TextInput(text=prompt)
    query_input = types.QueryInput(text=text_input, language_code=language_code)
    request = types.DetectIntentRequest(
        session=session_path, query_input=query_input
    )
    logger.log_text('session id {session_id} detecting intent with chatbot')
    response = session_client.detect_intent(request=request)
    logger.log_text('session id {session_id} response received')
    
            
    logger.log_text(f'session id {session_id} response: {response}')
    params_dict = dict(response.query_result.parameters)
    # params_dict = dict(response.parameters)
    logger.log_struct(params_dict)
    for key, value in params_dict.items():
        logger.log_text(f'session id {session_id} {key}:\n{value}\n')
    # response_type = params_dict['$request.generative.response-type']
    response_type = 'html'
    
    if 'success' in params_dict and params_dict['success'] == False:
        chat_response = NO_DATA_HTML
        logger.log_text('session id {session_id} overriding agent response with fail safe HTML')
    else:
        chat_response = params_dict['output']
    
    # content = '\n'.join(content_list)
    # logger.log_text(content)
    # if content == '':
    #     content = f'Apologies, I tried the following query but it returned no result'

    # log results to cloud storage for analytics
    log_ts = datetime.now().strftime('%Y%m%d %H%M%S')
    logs_params_list = list()
    
    for key, value in params_dict.items():
        if key != 'key':
            logs_params_list.append({'key': key, 'value':value})
    log_dict ={
        'timestamp':log_ts, 
        'user_prompt': response.query_result.text, 
        'response': chat_response, 
        'params':logs_params_list, 
        'sessionId': str(session_id),
        'agent': agent_id
        }

    gs_client = storage.Client()
    logs_bucket = gs_client.get_bucket(LOGS_BUCKET_NAME)
    log_blob = logs_bucket.blob(f'{LOGS_BLOB_PREFIX}{agent_id}_{log_ts}.json') 
    log_blob.upload_from_string(json.dumps(log_dict))

    return {'type':response_type, 'response':chat_response, 'sessionId': session_id}





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))