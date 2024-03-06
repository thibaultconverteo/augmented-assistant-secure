import os
from config import SERVICE_NAME


stream = os.popen(f'gcloud run deploy {SERVICE_NAME} --source . --region europe-west1')
output = stream.read()
print(output)