from flask_cors import CORS
from flask import Flask
import flask
import httplib2
from urllib.parse import quote

import os, json, re, time, uuid
from datetime import datetime
from numpy import random

from google.cloud import storage, logging, tasks_v2, bigquery
import vertexai
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
from vertexai.language_models import CodeGenerationModel
import google.auth

# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage

from utils import task
from config import SERVICE_NAME, SCOPES, HELLO_WORLD_HTML, SESSIONS_BUCKET_NAME, GENERATITVE_PROMPT, TABLE_SCHEMA, BQ_PROJECT_ID
from config import DATA_PROMT

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

gs_client = storage.Client()
sessions_bucket = gs_client.get_bucket(SESSIONS_BUCKET_NAME)

creds, project = google.auth.default(scopes=SCOPES)
vertexai.init(project=project_id, location="europe-west1")
    

# logging client
log_client = logging.Client()
logger = log_client.logger(log_name)
logger.default_resource = res

# cloud tasks client
ct_client = tasks_v2.CloudTasksClient()



@app.route("/processPrompt", methods=['GET', 'POST'])
def process_prompt():
    
    
    data = flask.request.data.decode()
    logger.log_text(f'request data {data}')
    params = json.loads(data)
    user_prompt = params.get('prompt')
    if user_prompt == '':
        logger.log_text('could not retrieve prompt')
        return {'type':response_type, 'response':HELLO_WORLD_HTML, 'sessionId': session_id}

    headers_dict = dict(flask.request.headers)
    logger.log_text(f'request headers {json.dumps(headers_dict)}')
    session_id = headers_dict.get('Sessionid')
    if session_id == '' or session_id is None:
        logger.log_text(f"could not retrieve session id from header, intializating one", severity='INFO')
        session_id = uuid.uuid4()
        step = 0
        session_status = {
                    'intent':None,
                    'result':None,
                    'response':None
                }
        
        session_log = {
            'session_id':session_id,
            'steps':[
                session_status
            ]
        }
    else:
        sessions_blob = sessions_bucket.get_blob(session_id)
        session_log = json.loads(sessions_blob.download_as_string().decode())
    logger.log_text(f"session id {session_id}", severity='INFO')

    
    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "intent": {"type": "STRING"},
                "sql_query": {"type": "STRING"},
                "html_code": {"type": "STRING"},
            },
            "required": [
                "intent",
                ],
        },
    }

    model = GenerativeModel("gemini-1.5-pro")
    # model = GenerativeModel("gemini-1.5-flash-001")
    generation_config = GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
            max_output_tokens=8092,
            temperature=0.1,
            top_p=1,
        )
    
    prompt = GENERATITVE_PROMPT.format(
        prompt=user_prompt,
        context_string="",
        csv_data_string="",
        last_sql_string="",
        table_schema=TABLE_SCHEMA
        )
    logger.log_text(f'prompt:\n{prompt}')
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )
    logger.log_text(response.text)

    json_response = json.loads(response.text)[0]

    intent = json_response['intent']
    if intent == 'sql':
        sql_query = json_response['sql_query']
        bq_client = bigquery.Client(project=BQ_PROJECT_ID)
        bq_result = bq_client.query(sql_query).result()
        result_rows = [row for row in bq_result]
        
        header_fields = result_rows[0].keys()
        header = ','.join([field for field in header_fields])
        data = '\n'.join([header]+[','.join(["%s"%result_row[field] for field in header_fields]) for result_row in result_rows])
        
    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "html_code": {"type": "STRING"},
            },
            "required": [
                "html_code",
                ],
        },
    }

    generation_config = GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
            max_output_tokens=8092,
            temperature=0.1,
            top_p=1,
        )
    
    
    prompt = DATA_PROMT.format(user_prompt=user_prompt, sql_result=data)
    logger.log_text(f'prompt:\n{prompt}')
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )
    logger.log_text(response.text)
    json_response = json.loads(response.text)[0]

    html_response = json_response['html_code']
    


    
    response_type = 'html'
    # chat_response = HELLO_WORLD_HTML
    
    return {'type':response_type, 'response':html_response, 'sessionId': session_id}





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))