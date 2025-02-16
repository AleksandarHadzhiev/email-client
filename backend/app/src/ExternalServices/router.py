from fastapi import APIRouter
from app.settings import Settings
from app.src.ExternalServices.controller import ExternalServicesController

class ExternalServiceRouter():
    
    def __init__(self, settings:Settings):
        
        self.settings = settings
        self.router = APIRouter()
        self.controller = ExternalServicesController(settings=settings)
        self.router.add_api_route("/login", self.controller.login, methods=["POST"])
        self.router.add_api_route("/auth", self.controller.auth, methods=["POST"])
        self.router.add_api_route("/get/mails", self.controller.get_mails, methods=["GET"])
        self.router.add_api_route("/mail/{id}", self.controller.get_mail, methods=["GET"])
        self.router.add_api_route("/send", self.controller.send_message, methods=["POST"])
