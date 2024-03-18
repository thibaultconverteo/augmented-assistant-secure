deploy:
python deploy.py


URL:
https://augmented-chatbot-demo-4o52ykz34a-ew.a.run.app

gcloud builds submit --tag europe-west1-docker.pkg.dev/c-augmented-chatbot/cloud-run-source-deploy/augmented-chatbot-demo:latest .
gcloud run deploy process-drive-files --image europe-west1-docker.pkg.dev/c-augmented-chatbot/cloud-run-source-deploy/c-augmented-chatbot:latest  --region europe-west1

frontend URL: https://ai-chatbot-4o52ykz34a-ew.a.run.app/