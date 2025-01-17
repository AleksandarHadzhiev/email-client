import json

from fastapi import APIRouter, Request, Response
from app.settings import Settings
from app.src.Login.service import LoginService

class LoginRouter():
    
    def __init__(self, settings:Settings):
        self.settings = settings
        self.router = APIRouter()
        self.service = LoginService(settings=settings)
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/auth", self.auth, methods=["POST"])
        self.router.add_api_route("/get/mails", self.get_mails, methods=["GET"])


    def set_sso(self, sso):
        self.sso = sso


    async def login(self, request: Request):
        body = await request.json()
        email = body["email"]
        self.service.set_login_factory(email=email)
        sso = self.service.get_sso()
        print(sso)
        self.set_sso(sso=sso)
        redirect_uri = await sso.login(request=request, email=email)
        print(self.sso)
        return redirect_uri


    async def auth(self, request: Request):
        username = await self.sso.callback(request)
        return username


    async def get_mails(self):
        messages = await self.sso.search_messages()
        return messages