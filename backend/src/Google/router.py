import json

from fastapi import APIRouter, Request, Response
from oauthlib.oauth2 import WebApplicationClient
from settings import Settings
from .service import GoogleService


class GoogleRouter:

    def __init__(self, settings:Settings):
        self.settings = settings
        self.google_service = GoogleService(settings) 
        self.router = APIRouter()
        self.client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)
        self.router.add_api_route("/google/login", self.login, methods=["GET"])
        self.router.add_api_route("/google/callback", self.callback, methods=["POST"])


    async def login(self):
        google_provider_cfg = self.google_service.get_google_provider_cfg()
        authorization_enpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = self.client.prepare_request_uri(
            authorization_enpoint,
            redirect_uri=self.settings.REDIRECT_URI,
            access_type = 'offline',
            prompt="consent",
            scope=self.settings.GOOGLE_SCOPES
        )
        return Response(content=json.dumps(request_uri), media_type="text/plain")
    
    
    async def callback(self, request: Request):
        body = await request.json()
        code = self.google_service.get_code_from_redirect_url(request_body=body)
        access_token = self.google_service.generate_access_token(code=code)
        user_info = self.google_service.get_user_info(access_token=access_token)
        return Response(content=json.dumps(user_info.json()),  media_type="text/plain")
