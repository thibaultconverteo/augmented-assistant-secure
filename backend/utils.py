from urllib.parse import quote
from config import SERVICE_NAME, BASE_URL, SERVICE_ACCOUNT_EMAIL, PROJECT_ID, GENERATITVE_PROMPT, TABLE_SCHEMA, MAX_TOKENS, TABLE_NAME
from google.cloud import logging

import json
from vertexai.preview.generative_models import GenerationConfig
from vertexai.language_models import CodeGenerationModel

# wrapper for task creation
def task(uri, method='POST', params=None, base_url=BASE_URL):
    task = {
    "http_request": {  # Specify the type of request.
        "http_method": method,
        "url": base_url+uri+'?'+'&'.join(["%s=%s"%(quote(str(key)), quote(str(value))) for key, value in params.items()]),  # The full url path that the task will be sent to.
        "oidc_token": {
            "service_account_email": SERVICE_ACCOUNT_EMAIL,
            "audience": base_url,
        },
    }
}
    return task


# log_name = SERVICE_NAME
# res = logging.Resource(
#     type="cloud_run_revision",
#     labels={
#         "project_id":PROJECT_ID,
#         "service_name":SERVICE_NAME
#         }
#     )

# log_client = logging.Client()
# logger = log_client.logger(log_name)
# logger.default_resource = res


def init_session(session_id, session_blob):
    if not session_blob.exists():
        session_log = {
            'session_id':session_id,
            'steps':[]
        }
        last_query = None
        current_data = None
        conversation_history = ''
        
    else:
        session_log = json.loads(session_blob.download_as_string().decode())
        last_query = session_log.get('last_query')
        current_data = session_log.get('current_data')
        
    conversation_history = '\n'.join([f"user:{step['prompt']}\nyou replied: {step['response']}" for step in session_log['steps']])
    return conversation_history, current_data, last_query, session_log
    
    

def get_prompt_response(conversation_history, current_data, last_query, model, date):
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

    
    generation_config = GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
            max_output_tokens=MAX_TOKENS,
            temperature=0.1,
            top_p=1,
        )
    
    data_context_string = f'During the conversation, the following data was retrieved:n{current_data}' if current_data is not None else ''
    last_query_string = f'The last SQL query you used was:\n{last_query}' if last_query is not None else ''
    prompt = GENERATITVE_PROMPT.format(
        date=date,
        conversation_history=conversation_history,
        data_context_string=data_context_string,
        last_query_string=last_query_string,
        table_schema=TABLE_SCHEMA,
        max_tokens=MAX_TOKENS,
        table_name=TABLE_NAME
        )
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )
    return response.text
    
        
def get_html_response(model, data_prompt):
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
    
    return model.generate_content(
        data_prompt,
        generation_config=generation_config,
    )
    
    