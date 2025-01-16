from fastapi import Request
from oauthlib.oauth2 import WebApplicationClient
from app.settings import Settings
from .service import GoogleService


class GoogleSSO:

    def __init__(self, settings:Settings):
        self.settings = settings
        self.client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)
        self.google_service = GoogleService(settings=self.settings, client=self.client) 


    async def login(self, request: Request=None, email: str=None):
        google_provider_cfg = self.google_service.get_google_provider_cfg()
        authorization_enpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = self.client.prepare_request_uri(
            authorization_enpoint,
            access_type= 'offline',
            prompt = 'consent',
            redirect_uri=self.settings.REDIRECT_URI,
            scope=self.settings.GOOGLE_SCOPES,
            login_hint=email
        )
        return request_uri
    
    
    async def callback(self, request: Request):
        body = await request.json()
        self.google_service.set_code_from_redirect_url(request_body=body)
        access_token = self.google_service.get_access_token(body["pathname"])
        user_info = self.google_service.get_user_info(access_token=access_token)
        self.email_service = self.google_service.gmail_authenticate()
        return user_info.json()["email"]


    async def search_messages(self):
        result = self.email_service.users().messages().list(userId='me').execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.email_service.users().messages().list(userId='me', pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages