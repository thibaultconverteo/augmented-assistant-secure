from flask_cors import CORS
from flask import Flask, jsonify, after_request
import flask
import httplib2
from urllib.parse import quote

import os, json, re, time
from uuid import uuid4
from datetime import datetime
from numpy import random

from google.cloud import storage, logging, bigquery
import vertexai
import google.auth

# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage
from vertexai.preview.generative_models import GenerativeModel
from utils import init_session, get_prompt_response, get_html_response
from config import SERVICE_NAME, SCOPES, HELLO_WORLD_HTML, SESSIONS_BUCKET_NAME, BQ_PROJECT_ID, DATA_PROMPT_THIBAULT, DATA_PROMPT_LORIS, NO_DATA_HTML, PRECISION_HTML, MAX_TOKENS, TABLE_HTML_TEMPLATE

app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "https://dev-assistant-secure-4o52ykz34a-ew.a.run.app", "supports_credentials": True}})
cors = CORS(app, resources={r"/processPrompt": {"origins": "https://dev-assistant-secure-4o52ykz34a-ew.a.run.app"}}) # Be specific with the route

# @app.after_request
# def after_request(response):
#     response.headers.add("Access-Control-Allow-Origin", "https://dev-assistant-secure-4o52ykz34a-ew.a.run.app/") # Replace with your frontend URL
#     response.headers.add("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
#     response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
#     return response


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



@app.route("/processPrompt", methods=['GET', 'POST'])
def process_prompt():
    if flask.request.method == 'OPTIONS':
        response = flask.make_response()
        response.headers.add('Access-Control-Allow-Origin', 'https://dev-assistant-secure-4o52ykz34a-ew.a.run.app, https://dev-assistant-secure-815180401364.europe-west1.run.app')
        response.headers.add("supports_credentials", "True")
        # response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization') # Add any other required headers
        return response
    
    headers_dict = dict(flask.request.headers)
    logger.log_text(f'request headers {json.dumps(headers_dict)}')

    request_data_string = flask.request.data.decode()
    logger.log_text(f'request data {request_data_string}')
    params = json.loads(request_data_string)


    # specific to tests for internal GA assistant    
    origin = headers_dict.get('Origin')
    logger.log_text(f'host {origin}')
    if origin is not None and origin.find('pprod') >= 0:
        logger.log_text('from pprod')
        data_prompt = DATA_PROMPT_LORIS
    elif (origin is not None and origin.find('test')) or origin == 'null'  >= 0:
        logger.log_text('from test')
        data_prompt = DATA_PROMPT_THIBAULT
    else:
        logger.log_text('undefined origin')
        data_prompt = DATA_PROMPT_LORIS
    # end specific

    
    user_prompt = params.get('prompt')
    if user_prompt == '':
        logger.log_text('could not retrieve prompt')
        return {'type':response_type, 'response':HELLO_WORLD_HTML, 'sessionId': session_id}


    session_id = params.get('sessionId')
    logger.log_text(f'session id from body {session_id}')
    if session_id is None:
        session_id = headers_dict.get('Sessionid')
        logger.log_text(f'session id from header {session_id}')

    
    # init session status
    if session_id is None:
        logger.log_text(f"could not retrieve session id from header, intializating one", severity='INFO')
        session_id = str(uuid4())
    logger.log_text(f"session id {session_id}", severity='INFO')
    session_blob = sessions_bucket.blob(session_id)
    conversation_history, current_data, last_query, session_log = init_session(session_id, session_blob)
    current_step_log = {
        'prompt':user_prompt
        }
    
    
    session_blob = sessions_bucket.blob(session_id)
    conversation_history += f'\nuser:{user_prompt}'
    
    response = get_prompt_response(conversation_history, current_data, last_query, model, today)
    logger.log_text(f'session id {session_id} genAI response:{response}')
    json_response = json.loads(response)[0]

    intent = json_response['intent']
    current_step_log['intent'] = intent
    sql_result = None
    if intent == 'sql':
        sql_query = json_response['sql_query']
        session_log['last_query'] = sql_query
        current_step_log['sql_query'] = sql_query
        try:
            bq_result = bq_client.query(sql_query).result()
            result_rows = [row for row in bq_result][:100] # TODO handle large volumes
            if len(result_rows)==0:
                current_data = ''
                sql_result = 'no data'
                logger.log_text(f'session id {session_id} request returned no results')
            else:
                header_fields = result_rows[0].keys()
                header = ','.join([field for field in header_fields])
                current_data = '\n'.join([header]+[','.join(["%s"%result_row[field] for field in header_fields]) for result_row in result_rows])
                sql_result = 'ok'
                log_response = 'here are the results'
        except Exception as e:
            error_message = e.message
            sql_result = 'error'
            current_data = ''
            logger.log_text(f'session id {session_id} received an error while running the query')
        
        
        if sql_result!='ok':
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
        else:
            table_html = "<thead><tr>{0}</tr></thead>".format(''.join([f"<th>{field_name}</th>" for field_name in header_fields]))
            table_html += "<tbody>{0}</tbody>".format(''.join(["<tr>"+''.join([f"<td>{field_value}</td>" for field_value in data_row])+"</tr>" for data_row in result_rows]))
            html_response = TABLE_HTML_TEMPLATE.format(table_html=table_html)
        
        current_step_log['data'] = current_data
        current_step_log['response'] = log_response
        session_log['current_data'] = current_data
                
    elif intent=='refine':
        refine_question = json_response['question']
        html_response = PRECISION_HTML.format(question=refine_question)
        log_response = refine_question
        current_step_log['response'] = refine_question
    elif intent == 'html': 
        prompt = data_prompt.format(conversation_history=conversation_history, sql_result=current_data, max_tokens=MAX_TOKENS)
        logger.log_text(f'session id {session_id}: {prompt}')
        html_response = get_html_response(model, prompt)
        json_response = json.loads(html_response.text)[0]
        html_response = json_response['html_code']
        current_step_log['html'] = html_response
        log_response = "here's the requested visual"
        current_step_log['response'] = log_response
    else:
        logger.log_text(f"session id {session_id}: if you're here something went wrong")
        

        

    session_log['steps'].append(current_step_log)
    session_blob.upload_from_string(json.dumps(session_log))
    response_type = 'html'
    # chat_response = HELLO_WORLD_HTML
    
    response = {'type':response_type, 'response':html_response, 'sessionId': session_id, 'Sessionid': session_id}
    logger.log_text(f'session id {session_id} response :{json.dumps(response)}')
    return jsonify(response)




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))