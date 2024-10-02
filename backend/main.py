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
from config import SERVICE_NAME, SCOPES, HELLO_WORLD_HTML, SESSIONS_BUCKET_NAME, GENERATITVE_PROMPT, TABLE_SCHEMA, BQ_PROJECT_ID, DATA_PROMPT, DATA_PROMPT_THIBAULT, DATA_PROMPT_LORIS, NO_DATA_HTML, PRECISION_HTML, MAX_TOKENS

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

bq_client = bigquery.Client(project=BQ_PROJECT_ID)

creds, project = google.auth.default(scopes=SCOPES)
vertexai.init(project=project_id, location="europe-west1")
model = GenerativeModel("gemini-1.5-pro")
    
today = datetime.now().strftime('%Y-%m-%d')
# logging client
log_client = logging.Client()
logger = log_client.logger(log_name)
logger.default_resource = res

# cloud tasks client
ct_client = tasks_v2.CloudTasksClient()



@app.route("/processPrompt", methods=['GET', 'POST'])
def process_prompt():
    
    
    data_string = flask.request.data.decode()
    logger.log_text(f'request data {data_string}')
    params = json.loads(data_string)
    user_prompt = params.get('prompt')
    session_id = params.get('sessionId')
    logger.log_text(f'session id from body {session_id}')
    if user_prompt == '':
        logger.log_text('could not retrieve prompt')
        return {'type':response_type, 'response':HELLO_WORLD_HTML, 'sessionId': session_id}

    headers_dict = dict(flask.request.headers)
    logger.log_text(f'request headers {json.dumps(headers_dict)}')
    # session_id = headers_dict.get('Sessionid')
    if session_id is None:
        session_id = headers_dict.get('Sessionid')
        logger.log_text(f'session id from header {session_id}')

    host = headers_dict.get('Host')
    logger.log_text(f'host {host}')
    if host is not None and host.find('pprod') >= 0:
        logger.log_text('from pprod')
        data_prompt = DATA_PROMPT_LORIS
    elif host is not None and host.find('test') >= 0:
        logger.log_text('from test')
        data_prompt = DATA_PROMPT_THIBAULT
    else:
        logger.log_text('undefined host')
        data_prompt = DATA_PROMPT_LORIS


    if session_id is None:
        logger.log_text(f"could not retrieve session id from header, intializating one", severity='INFO')
        session_id = str(uuid.uuid4())
        step = 0
        
        session_log = {
            'session_id':session_id,
            'steps':[]
        }
        last_query_string = ''
        data_context_string = ''
        conversation_history = f'conversation history:\nuser:{user_prompt}'
        sessions_blob = sessions_bucket.blob(session_id)
    else:
        sessions_blob = sessions_bucket.get_blob(session_id)
        session_log = json.loads(sessions_blob.download_as_string().decode())
        last_step = session_log['steps'][-1]
        last_query = session_log.get('last_query')
        if last_query is not None:
            last_query_string=f'\nat some point during the conversation, you wrote the following query:\n{last_query}'
        else:
            last_query_string=''
        data_string = session_log.get('current_data')
        if data_string is not None:
            data_context_string = f'\nduring the previous steps of the conversation, the following data was already retrieved:\n{data_string}'
        else:
            data_context_string = ''
        conversation_history = f'conversation history:\n'
        conversation_history += '\n'.join([f"user:{step['prompt']}\nyou replied: {step['response']}" for step in session_log['steps']])
        conversation_history += f'\nuser:{user_prompt}'
    
        
    logger.log_text(f"session id {session_id}", severity='INFO')

    
    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "intent": {"type": "STRING"},
                "sql_query": {"type": "STRING"},
                "html_code": {"type": "STRING"},
                "question": {"type": "STRING"},
            },
            "required": [
                "intent",
                ],
        },
    }

    
    # model = GenerativeModel("gemini-1.5-flash-001")
    generation_config = GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
            max_output_tokens=MAX_TOKENS,
            temperature=0.1,
            top_p=1,
        )
    
    prompt = GENERATITVE_PROMPT.format(
        date=today,
        conversation_history=conversation_history,
        data_context_string=data_context_string,
        last_query_string=last_query_string,
        table_schema=TABLE_SCHEMA,
        max_tokens=MAX_TOKENS
        )
    logger.log_text(f'session id {session_id} prompt:\n{prompt}')
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )
    logger.log_text(f'session id {session_id} genAI response:{response.text}')

    json_response = json.loads(response.text)[0]

    intent = json_response['intent']
    sql_result = None
    if intent == 'sql':
        sql_query = json_response['sql_query']
        session_log['last_query'] = sql_query
        
        try:
            bq_result = bq_client.query(sql_query).result()
            result_rows = [row for row in bq_result]
            if len(result_rows)==0:
                data_string = ''
                sql_result = 'no data'
                logger.log_text(f'session id {session_id} request returned no results')
            else:
                header_fields = result_rows[0].keys()
                header = ','.join([field for field in header_fields])
                data_string = '\n'.join([header]+[','.join(["%s"%result_row[field] for field in header_fields]) for result_row in result_rows])
                session_log['current_data'] = data_string
                sql_result = 'ok'
                log_response = 'here are the results'
        except Exception as e:
            error_message = e.message
            sql_result = 'error'
            logger.log_text(f'session id {session_id} received an error while running the query')
        
        
    
    if intent=='sql' and sql_result!='ok':
        if sql_result=='no data':
            html_response = NO_DATA_HTML.format(
                no_data_message_type='I am sorry, the query returned no results',
                sql_query=sql_query)
            log_response = "I am sorry, the query returned no results"
        elif sql_result=='error':
            html_response = NO_DATA_HTML.format(
                no_data_message_type=f'I am sorry, I received the following error:\n{error_message}',
                sql_query=sql_query)
            log_response = f'I am sorry, I received the following error:\n{error_message}'
        
    elif intent=='refine':
        question = json_response['question']
        html_response = PRECISION_HTML.format(question=question)
        log_response = question
    else:
    
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
                max_output_tokens=MAX_TOKENS,
                temperature=0.1,
                top_p=1,
            )
        
        
        prompt = data_prompt.format(conversation_history=conversation_history, sql_result=data_string, max_tokens=MAX_TOKENS)
        logger.log_text(f'session id {session_id} prompt:\n{prompt}')
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
        )
        logger.log_text(f'session id {session_id}: genAI response {response.text}')
        json_response = json.loads(response.text)[0]

        html_response = json_response['html_code']
        log_response = "here's the requested information"
        

    current_step_log = {
        'prompt':user_prompt,
        'intent':intent,
        'response':log_response
        }
    if intent=='sql':
        current_step_log['data'] = data_string,
        current_step_log['sql_query'] = sql_query
    elif intent=='refine':
        current_step_log['question'] = question
    session_log['steps'].append(current_step_log)

    sessions_blob.upload_from_string(json.dumps(session_log))
    response_type = 'html'
    # chat_response = HELLO_WORLD_HTML
    
    response = {'type':response_type, 'response':html_response, 'sessionId': session_id, 'Sessionid': session_id}
    logger.log_text(f'session id {session_id} response :{json.dumps(response)}')
    return response





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))