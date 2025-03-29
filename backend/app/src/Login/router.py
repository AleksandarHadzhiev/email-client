from fastapi import APIRouter
from app.settings import Settings
from app.src.Login.controller import LoginController

class LoginRouter():
    
    def __init__(self, settings:Settings):
        
        self.settings = settings
        self.router = APIRouter()
        self.controller = LoginController(settings=settings)
        self.router.add_api_route("/login", self.controller.login, methods=["POST"])
        self.router.add_api_route("/auth", self.controller.auth, methods=["POST"])
