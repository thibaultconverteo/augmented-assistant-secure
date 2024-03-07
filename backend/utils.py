from urllib.parse import quote
from config import SERVICE_NAME, BASE_URL, SERVICE_ACCOUNT_EMAIL

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



