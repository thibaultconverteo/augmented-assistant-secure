SERVICE_NAME = 'analytics-assistant-backend'
BASE_URL = 'https://analytics-assistant-backend-4o52ykz34a-ew.a.run.app'

SERVICE_ACCOUNT_EMAIL = '815180401364-compute@developer.gserviceaccount.com'
PROJECT_ID = 'c-augmented-chatbot'
BQ_PROJECT_ID = 'c-genai-sandbox-analytics'

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
  <h1>Hello World</h1>
</body>
</html>"""





GENERATITVE_PROMPT = """
you are an analytics assistant, with specific expertise of Google Analytics and it export model in BigQuery
The user's last question is: {prompt}
{context_string}
{csv_data_string}
{last_sql_string}
Depending on your interpretation of the question, either create a SQL query to match the user requirement, in which case reply with intent 'sql' 
and qrite the query 'sql_query'.
or create the HTML code that displays the data in csv_data if available, in which case reply with intent 'html' 
and qrite the html code in  'html_code'

if you create a html code:
The HTML code you produce will be rendered with no additional corrections, so it needs to be fully self contained.
The HTML code must be responsive.
The HTML code will be displayed in a dark background, adjust all colors accordingly.
Consider that the HTML code will be rendered in a 500x500 pixels frame by default


if you create a query, make sure that it is compliant with BigQuery SQL and with the table schema below
The target table is c-genai-sandbox-analytics.ia_generative_ga4.events_view_tl
It is imperative that you only refer to fields that are available in the table schema provided below. If you believe a field is not available, 
ignore the instruction to produce a SQL query and just reply that you do not know this field.
Keep in mind that fields with mode REPEATED require using the UNNEST operator.
Specifically, the device field does not require to be unnested.

Unless the user specifies a period, do not use any table suffixes or time partitions in the WHERE clause
If the user asks a question about products, use the items repeated field, and keep in mind that you need to use the UNNEST syntax .
Also, pay attention to the granularity required by the user. If they specify 'monthly' or 'per month', make sure that you produce a result that 
is agregated by month. same thing if the user asks for a weekly agregation.

Keep in mind that the current year is 2024.
If you create calculated fields, make sure to name them explicitly.

For example if the user wants to know what are the daily sales for each product, use:

SELECT
      event_date,
      items_flat.item_id,
      items_flat.item_name AS item_name,
      SUM(items_flat.item_revenue) AS item_revenue
FROM `c-genai-sandbox-analytics.ia_generative_ga4.events_view_tl` ,
      UNNEST (items) AS items_flat
group by 1, 2, 3

if the user asks about the conversion rate, the calculation is the number of sessions who have converted divided by the total number of sessions. 
You can use something like:
SELECT
  traffic_source.name AS source_name,
  COUNT(1) AS total_sessions,
  COUNT(DISTINCT
  IF
    (event_name = 'purchase', 1, NULL)) AS converted_sessions,
  COUNT(DISTINCT
  IF
    (event_name = 'purchase', 1, NULL)) / COUNT(1) AS conversion_rate
FROM
  `c-genai-sandbox-analytics.ia_generative_ga4.events_view_tl`

GROUP BY
  source_name


if the user mentions channel grouping, use the channel_grouping field

the table has the following schema
{table_schema}
"""


TABLE_SCHEMA = "{'fields': [{'name': 'event_date', 'type': 'DATE', 'mode': 'NULLABLE'}, {'name': 'event_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'event_params', 'type': 'RECORD', 'mode': 'REPEATED', 'fields': [{'name': 'key', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'value', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'string_value', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'int_value', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'float_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'double_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}]}]}, {'name': 'user_pseudo_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'device', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'category', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_brand_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_model_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_marketing_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'mobile_os_hardware_model', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'operating_system', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'operating_system_version', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'vendor_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'advertising_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'language', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'is_limited_ad_tracking', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'time_zone_offset_seconds', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'browser', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'browser_version', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'web_info', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'browser', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'browser_version', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'hostname', 'type': 'STRING', 'mode': 'NULLABLE'}]}]}, {'name': 'traffic_source', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'medium', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'source', 'type': 'STRING', 'mode': 'NULLABLE'}]}, {'name': 'ecommerce', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'total_item_quantity', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'purchase_revenue_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'purchase_revenue', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'refund_value_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'refund_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'shipping_value_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'shipping_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'tax_value_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'tax_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'unique_items', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'transaction_id', 'type': 'STRING', 'mode': 'NULLABLE'}]}, {'name': 'items', 'type': 'RECORD', 'mode': 'REPEATED', 'fields': [{'name': 'item_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_brand', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_variant', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category2', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category3', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category4', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_category5', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'price_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'price', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'quantity', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'item_revenue_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'item_revenue', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'item_refund_in_usd', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'item_refund', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'coupon', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'affiliation', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'location_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_list_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_list_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_list_index', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'promotion_id', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'promotion_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'creative_name', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'creative_slot', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'item_params', 'type': 'RECORD', 'mode': 'REPEATED', 'fields': [{'name': 'key', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'value', 'type': 'RECORD', 'mode': 'NULLABLE', 'fields': [{'name': 'string_value', 'type': 'STRING', 'mode': 'NULLABLE'}, {'name': 'int_value', 'type': 'INTEGER', 'mode': 'NULLABLE'}, {'name': 'float_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}, {'name': 'double_value', 'type': 'FLOAT', 'mode': 'NULLABLE'}]}]}]}, {'name': 'channel_grouping', 'type': 'STRING', 'mode': 'NULLABLE'}]}"


DATA_PROMT = """You are a front end developer tasked with writing HTML code that will adress the user question:
    {user_prompt}
    based on the following data:
    {sql_result}
    The HTML code you produce will be rendered with no additional corrections, so it needs to be fully self contained.
    The HTML code must be responsive.
    The HTML code will be displayed in a dark background, adjust all colors accordingly.
    Consider that the HTML code will be rendered in a 500x500 pixels frame by default."""