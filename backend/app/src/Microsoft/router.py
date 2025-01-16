import json
from urllib.parse import parse_qs, urlparse

import identity.web
from app.settings import Settings
from fastapi import APIRouter, Response, Request
from .service import MicrosoftService

class MicrosoftRouter:
    
    def __init__(self, settings: Settings):
        self.authority =f"https://login.microsoftonline.com/common"
        self.settings = settings
        self.router = APIRouter()
        self.service = MicrosoftService()
        self.router.add_api_route("/microsoft/login", self.login, methods=["GET"])
        self.router.add_api_route("/microsoft/response", self.auth_response, methods=["POST"])
        self.router.add_api_route("/microsoft/logout", self.logout, methods=["GET"])


    def set_auth(self, auth):
        self.auth = auth


    async def login(self, request: Request):
        auth = identity.web.Auth(
            session=request.session,
            authority=self.authority,
            client_id=self.settings.MICROSOFT_CLIENT_ID,
            client_credential=self.settings.MICROSOFT_CLIENT_SECRET
        )
        self.set_auth(auth=auth)
        response = auth.log_in(
            scopes=self.settings.MICROSOFT_SCOPE,
            redirect_uri=self.settings.REDIRECT_URI
        )

        return Response(content=json.dumps(response), media_type="text/plain")


    async def logout(self):
        return Response(content=self.auth.log_out(self.settings.FRONTEND_URL), media_type="text/plain")



    async def auth_response(self, request: Request):
        body = await request.json()
        login_data = self.service.get_data_for_login(request_body=body)
        result = self.auth.complete_log_in(login_data)
        user = self.auth.get_user()
        return Response(content=json.dumps(user), media_type="text/plain")
        