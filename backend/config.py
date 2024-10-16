PROJECT_ID = 'c-augmented-chatbot'
PROJECT_NUMBER = '579012253767'
REGION = 'europe-west1'
BQ_PROJECT_ID = 'plateforme-fournisseurs-dev'

SERVICE_NAME = 'dev-assistant-secure-backend'
BASE_URL = f'https://{SERVICE_NAME}-{PROJECT_NUMBER}-{REGION}.run.app'

SERVICE_ACCOUNT_EMAIL = f'{PROJECT_NUMBER}-compute@developer.gserviceaccount.com'


SESSIONS_BUCKET_NAME = 'c-augmented-chatbot-sessions-logs'
LOGS_BUCKET_NAME = 'c-augmented-chatbot-dialogflow-logs'
LOGS_BLOB_PREFIX = 'v2/'

TABLE_NAME = 'plateforme-fournisseurs-dev.c_dashboard.insights_ecommerces_agg'
TABLE_SCHEMA = """[{"mode":"NULLABLE","name":"date_evenement","type":"DATE"},{"mode":"NULLABLE","name":"enseigne","type":"STRING"},{"mode":"NULLABLE","name":"id_produit","type":"STRING"},{"mode":"NULLABLE","name":"ean","type":"STRING"},{"mode":"NULLABLE","name":"type_produit","type":"STRING"},{"mode":"NULLABLE","name":"ref_id_produit_concat","type":"STRING"},{"mode":"NULLABLE","name":"id_marque","type":"STRING"},{"mode":"NULLABLE","name":"id_segment","type":"INTEGER"},{"mode":"NULLABLE","name":"id_secteur","type":"INTEGER"},{"mode":"NULLABLE","name":"id_sous_secteur","type":"INTEGER"},{"mode":"NULLABLE","name":"id_famille","type":"INTEGER"},{"mode":"NULLABLE","name":"segment","type":"STRING"},{"mode":"NULLABLE","name":"secteur","type":"STRING"},{"mode":"NULLABLE","name":"sous_secteur","type":"STRING"},{"mode":"NULLABLE","name":"famille","type":"STRING"},{"mode":"NULLABLE","name":"ca_facture","type":"FLOAT"},{"mode":"NULLABLE","name":"nbr_transaction","type":"INTEGER"},{"mode":"NULLABLE","name":"nbr_quantite_achete","type":"INTEGER"},{"mode":"NULLABLE","name":"nbr_ajout_au_panier","type":"INTEGER"},{"mode":"NULLABLE","name":"nbr_vue","type":"INTEGER"}]"""

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
  <p>Hello World</p>
</body>
</html>"""





GENERATITVE_PROMPT = """
you are a data analyst, tasked with assisting business users in providing e-commerce insights.
The current date is {date}
conversation history:

{conversation_history}

{data_context_string}

{last_query_string}



Depending on your interpretation of the user input, either create a SQL query to match the user requirement, in which case reply with intent 'sql' 
and qrite the query 'sql_query'.
or create the HTML code that displays the data in csv_data if available, in which case just reply with intent html, the actual code will be produced later.

Keep in mind that users may ask questions that are too broad; if you believe that is the case, then reply with intent 'refine', 
and ask a question back to the user requesting additional precisions. store the question in 'question'.
For example: 
- the user should always specify a time period in his question, but you should also try to infer a period 
  from their question (e.g march to may would mean march 1st until may 31st)


if you create a query, make sure that it is compliant with BigQuery SQL and with the table schema below
The target table is {table_name}.
It is imperative that you only refer to fields that are available in the table schema provided below. 
If you believe a field is not available, ignore the instruction to produce a SQL query and just reply that you do not know this field.

Keep in mind that all descriptives field values are capitalized, so modify the user prompt to make sure that your query will match the correct values.

The table is partitioned on field date_evenement which has format DATE (therefore stored as YYY-MM-DD). As much as is possible, try to explicitly reduce the data scanned by leveraging the partitions, e.g include date_evenement between 'date a' and date b'.
when the result includes a time related field, make sure that you include an ORDER BY clause on the time field.



If you create calculated fields, make sure to name them explicitly.
Always round calculations to 2 decimal places.
Make sure that you include descriptive columns in your query (calendar periods for example)

If you implement a division as a calculation, always use the SAFE_DIVIDE operator to avoid division by zero.

the table has the following schema
{table_schema}
keep in mind that you are limited to {max_tokens} tokens
"""




DATA_PROMPT = """You are a front end developer tasked with writing HTML code that will adress the conversation you had with the user:
{conversation_history}

based on the following data:
{sql_result}
    
    Always use the Montserrat sans-serif font.
    The HTML code will potentially be displayed in either light or dark background, adjust all colors accordingly, and use a transparent background.
    The HTML code will be rendered in an iFrame, therefore:
      the code be fully self contained, with no dependencies.
      do not specify any formatting for your div as it is already taken care of by the iFrame
    keep in mind that you are limited to {max_tokens} tokens"""


DATA_PROMPT_LORIS = """You are a front end developer tasked with writing HTML code that will adress the conversation you had with the user:
{conversation_history}

based on the following data:
{sql_result}

Always use the Montserrat sans-serif font.
The HTML code will potentially be displayed in a dark background, adjust all colors accordingly.
The code be fully self contained, with no dependencies.
in order for the iframe to be rendered responsively, make sure to set the appropriate height property value in the body.
  
keep in mind that you are limited to {max_tokens} tokens"""

DATA_PROMPT_THIBAULT = """You are a front end developer tasked with writing HTML code that will adress the conversation you had with the user:
{conversation_history}

based on the following data:
{sql_result}

Always use the Montserrat sans-serif font.
The HTML code will be rendered in an iframe, on a dark background, so adjust colors accordingly.
Make sure that you do not escape double quote characters.
If you need to create visuals, use chart.js and import from https://cdn.jsdelivr.net/npm/chart.js.
Create the html so that the height is 400px, and make sure to set the "height" property accordingly.
If you create a visual, follow data visualization good practices, ie:
- make sure to include legends , axis descriptions etc...
- for time related data, use time series rather than bar charts
Use a pastel-inspired color palette, avoid bright, neon colors
keep in mind that you are limited to {max_tokens} tokens"""



NO_DATA_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
  <style>
    body {{
      font-family: 'Montserrat', sans-serif;
      background-color: black; /* Makes the background transparent */
      color: white; /* A mid-gray color for high contrast */
      height: 200px;
    }}
  </style>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
</head>
<body>
  <p>{no_data_message_type}</p>
  <p>Here is the query I was trying to run:</p>
  <p>{sql_query}</p>
</body>
</html>
"""

PRECISION_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
  <style>
    body {{
      font-family: 'Montserrat', sans-serif;
      background-color: black; /* Makes the background transparent */
      color: white; /* A mid-gray color for high contrast */
      height: 50px;
    }}
  </style>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
</head>
<body>
  <p>{question}</p>
</body>
</html>
"""


TABLE_HTML_TEMPLATE = """<!DOCTYPE html>
<html>

<head>
  <title>Conversion Rate</title>
  <style>
    body {{
      font-family: 'Montserrat', sans-serif;
      background-color: #333;
      color: #eee;
      height: 400px;
    }}

    table {{
      width: 80%;
      margin: 20px auto;
      border-collapse: collapse;
    }}

    th,
    td {{
      border: 1px solid #555;
      padding: 10px;
      text-align: left;
    }}

    th {{
      background-color: #444;
    }}
  </style>
</head>

<body>
  <table>
    {table_html}
  </table>
</body>

</html>"""