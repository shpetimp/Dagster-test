from google.oauth2.service_account import Credentials

def get_credentials_from_env():

    gcp_credentials = Credentials.from_service_account_file(
        "gcp_credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery"
        ]
    )

    return gcp_credentials