PROJECT_ID = 'c-augmented-chatbot'
PROJECT_NUMBER = '815180401364'
REGION = 'europe-west1'
BQ_PROJECT_ID = 'c-genai-sandbox-analytics'

SERVICE_NAME = 'pprod-analytics-assistant-backend'
BASE_URL = f'https://{SERVICE_NAME}-{PROJECT_NUMBER}-{REGION}.run.app'

SERVICE_ACCOUNT_EMAIL = '815180401364-compute@developer.gserviceaccount.com'


SESSIONS_BUCKET_NAME = 'c-augmented-chatbot-sessions-logs'
LOGS_BUCKET_NAME = 'c-augmented-chatbot-dialogflow-logs'

LOGS_BLOB_PREFIX = 'v2/'



# Google Drive parameters
# CLIENT_ID = ''
# CLIENT_SECRET = ''
# REFRESH_TOKEN = ''
SCOPES = ["https://www.googleapis.com/auth/cloud-platform",
          # "https://www.googleapis.com/auth/dialogflow"
          ]
PROVIDER = 'gemini'
LOCATION = 'us-central1'

MAX_TOKENS = 8092

HELLO_WORLD_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
  <style>
    body {
      font-family: 'Montserrat', sans-serif;
    }
  </style>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
</head>
<body>
  <h4>Hello World</h4>
</body>
</html>"""





GENERATITVE_PROMPT = """
you are an analytics assistant, with specific expertise of Google Analytics (GA4) and it export model in BigQuery.
The current date is {date}
{conversation_history}
{data_context_string}
{last_query_string}



Depending on your interpretation of the input, either create a SQL query to match the user requirement, in which case reply with intent 'sql' 
and qrite the query 'sql_query'.
or create the HTML code that displays the data in csv_data if available, in which case just reply with intent html, the actual code will be produced later.

Keep in mind that users may ask questions that are too broad; if you believe that is the case, then reply with intent 'refine', 
and ask a question back to the user requesting additional precisions. store the question in 'question'.
For example: 
- the user should always specify a time period in his question, but you should also try to infer a period 
  from their question (e.g march to may would mean march 1st until may 31st)
- If a user asks for a conversion rate, they should specify which conversion rate they have in mind


if you create a query, make sure that it is compliant with BigQuery SQL and with the table schema below
The target view is c-genai-sandbox-analytics.ia_generative_ga4.events_view_tl.
The view is almost entirely based on a GA4 Bigquery export with a few modifications.
It is imperative that you only refer to fields that are available in the table schema provided below. If you believe a field is not available, 
ignore the instruction to produce a SQL query and just reply that you do not know this field.
Keep in mind that fields with mode REPEATED require using the UNNEST operator.

The view you are querying is not partitioned or sharded, therefore do not use TABLE_SUFFIX or PARTITIONTIME in your query.
If you need to use a date field, use event_date which has BigQuery type DATE (and therefore stored as YYYY-MM-DD).
If the user asks a question about products, use the items repeated field, and keep in mind that you need to use the UNNEST syntax .
Also, pay attention to the granularity required by the user. If they specify 'monthly' or 'per month', make sure that you produce a result that 
is agregated by month. same thing if the user asks for a weekly agregation.



If you create calculated fields, make sure to name them explicitly.
Always round calculations to 2 decimal places.
Make sure that you include in your query descriptive columns (calendar periods for example)

If you implement a division as a calculation, always use the SAFE_DIVIDE operator to avoid division by zero.

if the user wants to know what are the daily sales for each product, use:

SELECT
      event_date,
      items_flat.item_id,
      items_flat.item_name AS item_name,
      SUM(items_flat.item_revenue) AS item_revenue
FROM `c-genai-sandbox-analytics.ia_generative_ga4.events_view_tl` ,
      UNNEST (items) AS items_flat
group by 1, 2, 3


if the user mentions channel grouping, use the channel_grouping field

the table has the following schema
{table_schema}
keep in mind that you are limited to {max_tokens} tokens
"""


TABLE_SCHEMA = "{'fields': [{'name': 'event_date', 'type': 'DATE', 'mode': 'NULLABLE'}, {'name': 'event_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'event_params', 'type': 'RECORD', 'mode': 'REPEATED', 'fields': [{'name': 'key', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'value', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'string_value', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'int_value', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'float_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'double_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}]}]}, {'name': 'user_pseudo_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'device', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'category', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_brand_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_model_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_marketing_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_os_hardware_model', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'operating_system', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'operating_system_version', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'vendor_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'advertising_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'language', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'is_limited_ad_tracking', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'time_zone_offset_seconds', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'browser', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'browser_version', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'web_info', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'browser', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'browser_version', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'hostname', 'type': 'STRING', 'mode': 'NULLABLE'}]}]}, {'name': 'traffic_source', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'medium', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'source', 'type': 'STRING', 'mode': 'NULLABLE'}]}, {'name': 'ecommerce', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'total_item_quantity', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'purchase_revenue_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'purchase_revenue', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'refund_value_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'refund_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'shipping_value_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'shipping_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'tax_value_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'tax_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'unique_items', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'transaction_id', 'type': 'STRING', 'mode': 'NULLABLE'}]}, {'name': 'items', 'type': 'RECORD', 'mode': 'REPEATED', 'fields': [{'name': 'item_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_brand', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_variant', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category2', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category3', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category4', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category5', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'price_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'price', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'quantity', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'item_revenue_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'item_revenue', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'item_refund_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'item_refund', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'coupon', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'affiliation', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'location_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_list_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_list_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_list_index', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'promotion_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'promotion_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'creative_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'creative_slot', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_params', 'type': 'RECORD', 'mode': 'REPEATED', 'fields': [{'name': 'key', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'value', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'string_value', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'int_value', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'float_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'double_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}]}]}]}, {'name': 'channel_grouping', 'type': 'STRING', 'mode': 'NULLABLE'}]}"


DATA_PROMPT = """You are a front end developer tasked with writing HTML code that will adress the conversation you had with the user:
    {conversation_history}
    based on the following data:
    {sql_result}
    Always use the roboto sans-serif font.
    The HTML code will potentially be displayed in either light or dark background, adjust all colors accordingly, and use a transparent background.
    The HTML code will be rendered in an iFrame, therefore:
      the code be fully self contained, with no dependencies.
      do not specify any formatting for your div as it is already taken care of by the iFrame
    keep in mind that you are limited to {max_tokens} tokens"""


DATA_PROMPT_LORIS = """You are a front end developer tasked with writing HTML code that will adress the conversation you had with the user:
    {conversation_history}
    based on the following data:
    {sql_result}
    Always use the roboto sans-serif font.
    The HTML code will potentially be displayed in a dark background, adjust all colors accordingly.
    The code be fully self contained, with no dependencies.
      
    keep in mind that you are limited to {max_tokens} tokens"""

DATA_PROMPT_THIBAULT = """You are a front end developer tasked with writing HTML code that will adress the conversation you had with the user:
    {conversation_history}
    based on the following data:
    {sql_result}
    Always use the roboto sans-serif font.
    The HTML code will potentially be displayed in either light or dark background, adjust all colors accordingly, and use a transparent background.
    The HTML code will be rendered in an iFrame, therefore:
      the code be fully self contained, with no dependencies.
      do not specify any formatting for your div as it is already taken care of by the iFrame
    keep in mind that you are limited to {max_tokens} tokens"""



NO_DATA_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
  <style>
    body {{
      font-family: 'Montserrat', sans-serif;
      background-color: transparent; /* Makes the background transparent */
      color: #808080; /* A mid-gray color for high contrast */
    }}
  </style>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
</head>
<body>
  <h4>{no_data_message_type}.</h4>
  <h4>Here is the query I was trying to run:</h4>
  <h4>{sql_query}</h4>
</body>
</html>
"""

PRECISION_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
  <style>
    body {{
      font-family: 'Roboto', sans-serif;
      background-color: transparent; /* Makes the background transparent */
      color: #808080; /* A mid-gray color for high contrast */
    }}
  </style>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
</head>
<body>
  <h4>{question}</h4>
</body>
</html>
"""

PRECISION_HTML = """<!DOCTYPE html>
<html>
<body>
  <h4>{question}</h4>
</body>
</html>
"""


