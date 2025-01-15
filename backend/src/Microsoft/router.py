import json
from urllib.parse import parse_qs, urlparse

import identity.web
from settings import Settings
from fastapi import APIRouter, Response, Request
from werkzeug.datastructures import ImmutableMultiDict

class MicrosoftRouter:
    
    def __init__(self, settings: Settings):
        self.authority =f"https://login.microsoftonline.com/common"
        self.settings = settings
        self.router = APIRouter()
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
        print(self.settings.REDIRECT_URI)
        response = auth.log_in(
            scopes=self.settings.MICROSOFT_SCOPE,
            redirect_uri=self.settings.REDIRECT_URI
        )

        return Response(content=json.dumps(response), media_type="text/plain")


    async def logout(self):
        return Response(content=self.auth.log_out(self.settings.FRONTEND_URL), media_type="text/plain")



    async def auth_response(self, request: Request):
        body = await request.json()
        print(body)
        pathname = body["pathname"]
        parse_res = urlparse(pathname)
        query_params = parse_qs(parse_res.query)
        input = ImmutableMultiDict(
            [
                ('code', query_params["code"][0]),
                ('client_info', query_params["client_info"][0]),
                ('state', query_params["state"][0]),
            ]
        )
        print(input)
        result = self.auth.complete_log_in(input)
        print(result)
        user = self.auth.get_user()
        print(user)
        return Response(content=json.dumps(user), media_type="text/plain")
        