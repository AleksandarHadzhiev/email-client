import json
import requests
from datetime import datetime, timedelta
from urllib import parse
from fastapi import Request
from app.settings import Settings
from oauthlib.oauth2 import WebApplicationClient
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Service():
    
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


    def get_required_data_for_complete_auth(self, authorization_response):
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
        response = token_response.json()
        return {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "expires_in": response["expires_in"],
        }


    def get_user_info(self, access_token):
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        return user_info
