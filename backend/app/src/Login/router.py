import json

from fastapi import APIRouter, Request, BackgroundTasks
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
        self.router.add_api_route("/mail/{id}", self.get_mail, methods=["GET"])
        self.router.add_api_route("/send", self.send_message, methods=["POST"])


    def set_sso(self, sso):
        self.sso = sso


    async def send_message(self, request: Request):
        body = await request.json()
        return self.sso.send_message(body=body)


    async def login(self, request: Request):
        body = await request.json()
        email = body["email"]
        self.service.set_login_factory(email=email)
        sso = self.service.get_sso()
        self.set_sso(sso=sso)
        redirect_uri = await sso.login(request=request, email=email)
        return redirect_uri


    async def auth(self, request: Request):
        username = await self.sso.callback(request)
        return username


    async def get_mails(self, background_tasks: BackgroundTasks):
        messages = await self.sso.search_messages(background_tasks)
        return messages


    async def get_mail(self, id:int):
        email = self.sso.read_message(id=id)
        return email