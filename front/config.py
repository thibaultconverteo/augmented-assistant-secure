PROJECT_ID = 'c-augmented-chatbot'
PROJECT_NUMBER = '815180401364'
REGION = 'europe-west1'
BQ_PROJECT_ID = 'c-genai-sandbox-analytics'

SERVICE_NAME = 'test-analytics-assistant'
# BASE_URL = f'https://{SERVICE_NAME}-{PROJECT_NUMBER}-{REGION}.run.app'


IMAGE_NAME = f'{REGION}-docker.pkg.dev/{PROJECT_ID}/cloud-run-source-deploy/{SERVICE_NAME}:latest'
SERVICE_ACCOUNT_EMAIL = '30048738242-compute@developer.gserviceaccount.com'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/bigquery',
    'https://www.googleapis.com/auth/cloud-vision'
]


HELLO_WORLD_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
</head>
<body>
  <h4>Hello, world!</h4>
</body>
</html>"""