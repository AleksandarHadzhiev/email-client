import json
from fastapi import Request, BackgroundTasks, Response
from oauthlib.oauth2 import WebApplicationClient
from app.settings import Settings
from .service import GoogleService


class GoogleSSO:

    def __init__(self, settings:Settings):
        self.settings = settings
        self.client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)
        self.google_service = GoogleService(settings=self.settings, client=self.client) 
        self.fetched_messages = []
        self.next_page_token = ""


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


    async def search_messages(self, background_tasks: BackgroundTasks):
        result = self._get_message_id_from_google()
        messages = self._fetch_all_messages(result=result)
        emails = self._read_messages_to_get_payload(messages=messages)
        self._extend_fetched_messages_until_length_fifty(emails=emails)
        self._set_next_page_token(result=result)
        return Response(content=json.dumps(self.fetched_messages), media_type="json")


    def _get_message_id_from_google(self):
        if self.next_page_token == "":
            result = self.email_service.users().messages().list(userId='me', maxResults=1).execute()
        else:
            result = self.email_service.users().messages().list(userId='me', pageToken=self.next_page_token, maxResults=1).execute()
        return result


    def _fetch_all_messages(self, result):
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        return messages


    def _read_messages_to_get_payload(self, messages) -> list:
        emails=[]
        for msg in messages:
            email = self.google_service.get_email_data(id=msg["id"], email_service=self.email_service)
            emails.append(email)
        return emails


    def _extend_fetched_messages_until_length_fifty(self, emails):
        if len(self.fetched_messages) <50:
            self.fetched_messages.extend(emails)


    def _set_next_page_token(self, result):
        if 'nextPageToken' in result:
            self.next_page_token = result['nextPageToken']
        else:
            self.next_page_token = ""


    def read_message(self, id:int):
        email = self.google_service.get_email_data(id=id)
        return email


    def send_message(self, body):
        return self.email_service.users().messages().send(
            userId="me",
            body = self.google_service.send_message(email_service=self.email_service, body=body)
        ).execute()