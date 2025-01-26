import base64
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from base64 import urlsafe_b64decode, urlsafe_b64encode

class Email():    
    def __init__(self, id, email_service):
        self.id = id
        self.email_service = email_service
        self.sender = ""
        self.subject = ""
        self.date = ""


    def build_message(self, body):
        print(body)
        message = MIMEText(body["body"])
        message['To'] = body["to"]
        message['From'] = body["from"]
        message['Subject'] = body["subject"]
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
        

    def get_email_content_for_microsoft(self, incoming_email):
        body = incoming_email["body"]["content"]
        soup = BeautifulSoup(body, "lxml")
        self.body = str(soup.body)
        self.body_preview = incoming_email["bodyPreview"]
        self.date = incoming_email["receivedDateTime"]
        self.sender = incoming_email["sender"]["emailAddress"]["name"] + "<" + incoming_email["sender"]["emailAddress"]["address"] + ">"
        self.subject = incoming_email["subject"]
        return {
            "from": self.sender,
            "date": self.date,
            "subject": self.subject,
            "body_preview": self.body_preview,
            "body": self.body
        }
    

    def get_email_content_for_gmail(self):
        headers_message = self.email_service.users().messages().get(userId='me', id=self.id).execute()
        self._set_email(headers_message=headers_message)
        return {
            "from": self.sender,
            "date": self.date,
            "subject": self.subject,
            "body_preview": self.body_preview,
            "body": self.body
        }


    def _set_email(self, headers_message):
        payload = headers_message["payload"]
        self.body_preview = headers_message["snippet"]
        mime_type = payload["mimeType"]
        self._set_headers(payload=payload)
        self.body = self._get_body_html_content(mime_type=mime_type, payload=payload)


    def _set_headers(self, payload):
        headers = payload["headers"]
        self._loop_through_headers(headers=headers)


    def _loop_through_headers(self, headers):
        for d in headers:
            self._assing_values(d=d)


    def _assing_values(self, d):
        if self.subject != "" and self.sender != "" and self.date != "":
            return
        elif d["name"] == 'Subject':
            self.subject = d['value']
        elif d['name'] == 'From':
            self.sender = d['value']
        elif d["name"] == "Date":
            self.date = d["value"]


    def _get_body_html_content(self, mime_type, payload):
        if mime_type == 'multipart/alternative':
            return self._loop_through_parts(payload=payload)
        elif mime_type == "multipart/mixed":
            return self._loop_through_parts(payload=payload)
        elif mime_type == "multipart/report":
            return self._loop_through_parts(payload=payload)
        elif mime_type != 'multipart/alternative':
            return self._get_body_through_decoding(part=payload)


    def _loop_through_parts(self,payload):
        parts = payload["parts"]
        body = ""
        part_index = 0
        # Multiple parts, so have to go through all of them.
        if len(parts) > 1:
            part_index = 1
        part = parts[part_index]
        soup = self._get_body_through_decoding(part=part)
        body += str(soup)
        return body


    def _get_body_through_decoding(self,part): 
        payload_body = part["body"]
        data = payload_body["data"]
        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode(data)
        soup = BeautifulSoup(decoded_data, "lxml")
        return str(soup.body)
