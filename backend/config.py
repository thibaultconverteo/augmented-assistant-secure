SERVICE_NAME = 'augmented-chatbot-demo'
BASE_URL = 'https://augmented-chatbot-demo-4o52ykz34a-ew.a.run.app'
SERVICE_ACCOUNT_EMAIL = '815180401364-compute@developer.gserviceaccount.com'
PROJECT_ID = 'c-augmented-chatbot'

LOGS_BUCKET_NAME = 'c-augmented-chatbot-dialogflow-logs'
LOGS_BLOB_PREFIX = 'v1/'
# BUCKET_NAME = 'c-robert-sandbox-drive-content'
# US_BUCKET_NAME = 'c-robert-sandbox-drive-content-us'


AGENT_ID = "bcc2db95-6313-4c62-bc06-f7f2a11b3c24" # v3
AGENT_ID = "0919046b-b61d-4e2f-8e15-f221fbb1ad47" # version new table
# Maximum number of pages processed by cloud vision API
# https://cloud.google.com/python/docs/reference/vision/latest/google.cloud.vision_v1.services.image_annotator.ImageAnnotatorClient#google_cloud_vision_v1_services_image_annotator_ImageAnnotatorClient_batch_annotate_files
CHUNK_SIZE = 5

# Google Drive parameters
# CLIENT_ID = ''
# CLIENT_SECRET = ''
# REFRESH_TOKEN = ''
SCOPES = ["https://www.googleapis.com/auth/cloud-platform",
          "https://www.googleapis.com/auth/dialogflow"]
PROVIDER = 'gemini'
LOCATION = 'us-central1'

NO_DATA_HTML = """<!DOCTYPE html>
<html>
    <style>
        body {
          background-color: #212121;
          color: #ffffff;
          font-family: 'Montserrat', sans-serif;
        }
    
        
      </style>
<head>
  <title>No Results Found</title>
</head>
<body>
  <h1>No results found.</h1>
  <p>Your request did not match any data in the table(s).</p>
</body>
</html>"""

FAIL_SAFE_HTML = """<!DOCTYPE html>
<html>
<head>
<title>Funny Insight</title>
<script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-base.min.js"></script>
<script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-pie.min.js"></script>
</head>
<body>
<div id="chart"></div>

<script type="text/javascript">
anychart.onDocumentReady(function() {
 var chart = anychart.pie([
 {x: "HTML", value: 40},
 {x: "CSS", value: 30},
 {x: "JavaScript", value: 30}
 ]);

 chart.title("I'm sorry I could not generate the requested HTML, but here's something else that might interest you");
 chart.legend().enabled(true);
 chart.legend().fontSize(15);
 chart.legend().padding([0, 0, 15, 0]);
 chart.container("chart");
 chart.draw();
});
</script>

<p>This chart shows the breakdown of a web page's components, which is quite ironic because the HTML code is supposed to generate a chart, but instead, it's displaying a chart that tells us that it couldn't generate the requested HTML. The chart is funny because it's a visual representation of the very thing it's failing to do.</p>
</body>
</html>"""