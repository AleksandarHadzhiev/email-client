from fastapi import Request
from oauthlib.oauth2 import WebApplicationClient
from app.settings import Settings
from .service import GoogleService


class GoogleSSO:

    def __init__(self, settings:Settings):
        self.settings = settings
        self.google_service = GoogleService(settings) 
        self.client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)


    async def login(self, request: Request=None, email: str=None):
        google_provider_cfg = self.google_service.get_google_provider_cfg()
        authorization_enpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = self.client.prepare_request_uri(
            authorization_enpoint,
            redirect_uri=self.settings.REDIRECT_URI,
            scope=self.settings.GOOGLE_SCOPES,
            login_hint=email
        )
        return request_uri
    
    
    async def callback(self, request: Request):
        body = request
        code = self.google_service.get_code_from_redirect_url(request_body=body)
        access_token = self.google_service.generate_access_token(code=code)
        user_info = self.google_service.get_user_info(access_token=access_token)
        return user_info.json()["email"]
