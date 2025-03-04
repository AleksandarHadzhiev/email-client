import json
import requests
from datetime import datetime, timedelta
from urllib import parse
from app.settings import Settings
from oauthlib.oauth2 import WebApplicationClient
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.src.modules.email import Email


class GoogleService():
    
    def __init__(self, settings: Settings, client: WebApplicationClient):
        self.settings = settings
        self.client = client
        self.token_url = "https://accounts.google.com/o/oauth2/token"


    def get_google_provider_cfg(self):
        return requests.get(self.settings.DISCOVERY_URL).json()


    def set_code_from_redirect_url(self, request_body):
        pathname = request_body["pathname"]
        parsed_url = parse.urlparse(pathname)
        code = parse.parse_qs(parsed_url.query)["code"][0]
        self.code = code


    def get_access_token(self, authorization_response):
        google_provider_cfg = self.get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=authorization_response,
            redirect_url=self.settings.REDIRECT_URI,
            code = self.code
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(self.settings.GOOGLE_CLIENT_ID, self.settings.GOOGLE_CLIENT_SECRET),
        )
        
        self.client.parse_request_body_response(json.dumps(token_response.json()))
        self._set_required_values_for_mail_creds(token_response=token_response.json())
        return token_response.json()["access_token"]


    def _set_required_values_for_mail_creds(self, token_response):
        self.access_token = token_response["access_token"]
        self.refresh_token = token_response["refresh_token"]
        self.expires_in = token_response["expires_in"]


    def get_user_info(self, access_token):
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        return user_info


    def get_mail_creds(self):
        token_uri = "https://oauth2.googleapis.com/token"
        expires_in = self.calculate_expiry()
        return Credentials(
            token=self.access_token,
            token_uri=token_uri,
            refresh_token=self.refresh_token,
            client_id=self.settings.GOOGLE_CLIENT_ID,
            client_secret=self.settings.GOOGLE_CLIENT_SECRET,
            account="",
            expiry=expires_in,
            scopes=self.settings.GOOGLE_SCOPES
        )


    def calculate_expiry(self):
        now = datetime.now()
        expiry = now + timedelta(seconds=self.expires_in)
        return expiry


    def gmail_authenticate(self):
        creds = self.get_mail_creds()
        service = None
        try:
            service = build("gmail", "v1", credentials=creds)
        except HttpError as error:
            raise error
        return service
    
    
    def get_email_data(self, id, email_service):
        email = Email(id=id, email_service=email_service)
        formated_email = email.get_email_content_for_gmail()
        return formated_email


    def send_message(self, email_service, body):
        email = Email("2123", email_service=email_service)
        return email.build_message(body)