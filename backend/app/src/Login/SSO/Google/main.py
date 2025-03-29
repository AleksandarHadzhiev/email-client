from fastapi import Request
from oauthlib.oauth2 import WebApplicationClient
from app.src.Login.SSO.Google.service import Service
from app.src.Login.SSO.SSO_provider import SSOProvider

class GoogleProvider(SSOProvider):
    
    def __init__(self, settings):
        super().__init__(settings)
        self.client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)
        self.google_service = Service(settings=self.settings, client=self.client) 
        self.fetched_messages = []
        self.next_page_token = ""


    async def login(self, data: dict=None, request: Request=None):
        google_provider_cfg = self.google_service.get_google_provider_cfg()
        authorization_enpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = self.client.prepare_request_uri(
            authorization_enpoint,
            access_type= 'offline',
            prompt = 'consent',
            redirect_uri=self.settings.REDIRECT_URI,
            scope=self.settings.GOOGLE_SCOPES,
            login_hint=data["email"]
        )
        return {"redirect_uri": request_uri}


    async def auth(self, request: Request):
        body = await request.json()
        self.google_service.set_code_from_redirect_url(request_body=body)
        required_data = self.google_service.get_required_data_for_complete_auth(body["pathname"])
        print("REQUIRED DATA: ")
        print(required_data)
        user_info = self.google_service.get_user_info(access_token=required_data["access_token"])
        response = required_data
        response["email"] = user_info.json()["email"] 
        response["type"] = "google"
        print(response)
        return response


