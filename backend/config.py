SERVICE_NAME = 'augmented-chatbot-demo'
BASE_URL = 'https://augmented-chatbot-demo-4o52ykz34a-ew.a.run.app'
SERVICE_ACCOUNT_EMAIL = '815180401364-compute@developer.gserviceaccount.com'
# BUCKET_NAME = 'c-robert-sandbox-drive-content'
# US_BUCKET_NAME = 'c-robert-sandbox-drive-content-us'

# Maximum number of pages processed by cloud vision API
# https://cloud.google.com/python/docs/reference/vision/latest/google.cloud.vision_v1.services.image_annotator.ImageAnnotatorClient#google_cloud_vision_v1_services_image_annotator_ImageAnnotatorClient_batch_annotate_files
CHUNK_SIZE = 5

# Google Drive parameters
CLIENT_ID = '111103087873-ttslctbg0queio3gtoh11tb2ttooegse.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REFRESH_TOKEN = '1//04oolhEP8BgfjCgYIARAAGAQSNwF-L9IrhuIuE-CsvUojwCQImcONPNRR5d2BX7qqKJ2PeKbjWGCfL59vCzTHvOG3v-s4ribw0nQ'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/cloud-platform', 
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/bigquery',
          'https://www.googleapis.com/auth/cloud-vision',
          'https://www.googleapis.com/auth/cloud-vision']


PROVIDER = 'gemini'

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