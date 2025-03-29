from datetime import datetime, timedelta
import logging
from app.src.Email.email_provider import EmailProvider
from app.src.modules.email import Email
from fastapi import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Google(EmailProvider):
    
    def __init__(self, settings):
        super().__init__(settings)
        self.fetched_messages = []
        self.next_page_token = ""


    def set_data_for_mail_creds(self, creds):
        self.access_token = creds["access_token"]
        self.refresh_token =  creds["refresh_token"]
        self.expires_in =  creds["expires_in"]


    def _get_mail_creds(self):
        token_uri = "https://oauth2.googleapis.com/token"
        expires_in = self.calculate_expiry()
        return Credentials(
            token=self.access_token,
            token_uri=token_uri,
            refresh_token=self.refresh_token,
            client_id=self.settings.GOOGLE_CLIENT_ID,
            client_secret=self.settings.GOOGLE_CLIENT_SECRET,
            account="",
            expiry=expires_in,
            scopes=self.settings.GOOGLE_SCOPES
        )


    def calculate_expiry(self):
        now = datetime.now()
        expiry = now + timedelta(seconds=int(self.expires_in))
        return expiry


    def _gmail_authenticate(self):
        creds = self._get_mail_creds()
        service = None
        try:
            service = build("gmail", "v1", credentials=creds)
        except HttpError as error:
            raise error
        return service



    def _build_email_service(self):
        service = None
        try:
            service = self._gmail_authenticate()
        except:
            logging.exception("Failed to build service")
        self.service = service


    async def send_email(self, data):
        print(self.service)
        email = Email("2123", email_service=self.service)
        _body = email.build_message(data)
        google_response =  self.service.users().messages().send(
            userId="me",
            body = _body
        ).execute()
        labels: list = google_response['labelIds']
        if 'SENT' in labels:
            return {"status": 'SENT'}
        return {"status": 'FAIL'}


    async def get_emails(self):
        self._build_email_service()
        result = self._get_message_id_from_google()
        messages = self._fetch_all_messages(result=result)
        emails = self._read_messages_to_get_payload(messages=messages)
        self._extend_fetched_messages_until_length_fifty(emails=emails)
        self._set_next_page_token(result=result)
        return self.fetched_messages


    def _get_message_id_from_google(self):
        if self.next_page_token == "":
            result = self.service.users().messages().list(userId='me', maxResults=1).execute()
            # self.next_page_token = result["messages"]["nextPageToken"]
        else:
            result = self.service.users().messages().list(userId='me', pageToken=self.next_page_token, maxResults=1).execute()
        return result


    def _fetch_all_messages(self, result):
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        return messages


    def _read_messages_to_get_payload(self, messages) -> list:
        emails=[]
        for msg in messages:
            email = Email(id=msg["id"], email_service=self.service)
            formated_email = email.get_email_content_for_gmail()
            emails.append(formated_email)
        return emails


    def _extend_fetched_messages_until_length_fifty(self, emails):
        if len(self.fetched_messages) <50:
            self.fetched_messages.extend(emails)


    def _set_next_page_token(self, result):
        if 'nextPageToken' in result:
            self.next_page_token = result['nextPageToken']
        else:
            self.next_page_token = ""


    async def get_email_by_id(self, id):
        email = Email(id=id, email_service=self.service)
        formated_email = email.get_email_content_for_gmail()
        return formated_email