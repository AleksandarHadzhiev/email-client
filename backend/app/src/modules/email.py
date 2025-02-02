import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from fastapi.responses import FileResponse

import mimetypes

import requests

class Email():    
    def __init__(self, id, email_service):
        self.id = id
        self.email_service = email_service
        self.sender = ""
        self.subject = ""
        self.date = ""
        self.attachments = []


    def build_message(self, body):
        print(body)
        
        if 'attachments' in body:
            message = self._attach_attachments(body=body)
        else:
            message = self._message_without_attachments(body=body)
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}  


    def _message_without_attachments(self, body):
        message = MIMEText(body["body"])
        self._set_basic_info(message=message, body=body)
        return message


    def _set_basic_info(self, message, body):
        message['To'] = body["to"]
        message['From'] = body["from"]
        message['Subject'] = body["subject"]
 

    def _attach_attachments(self, body):
        attachments = body['attachments']
        message = MIMEMultipart()
        self._set_basic_info(message=message, body=body)
        message.attach(MIMEText(body["body"]))
        for attachment in attachments:
            self._generate_attachment(attachment=attachment, message=message)
        return message  


    def _generate_attachment(self, attachment, message):
        main_type, sub_type = attachment["type"].split('/', 1)
        content = attachment["content"]
        print(content)
        if main_type == 'text':
            msg = MIMEText(content, _subtype =sub_type)
        elif main_type == "image":
            content = str(content).encode() 
            msg = MIMEImage(content, _subtype =sub_type)
        msg.add_header('Content-Disposition', 'attachment', filename=attachment["name"])
        message.attach(msg)


    def get_email_content_for_microsoft(self, incoming_email, headers):
        body = incoming_email["body"]["content"]
        soup = BeautifulSoup(body, "lxml")
        self.body = str(soup.body)
        self.body_preview = incoming_email["bodyPreview"]
        self.date = incoming_email["receivedDateTime"]
        self.sender = incoming_email["sender"]["emailAddress"]["name"] + "<" + incoming_email["sender"]["emailAddress"]["address"] + ">"
        self.subject = incoming_email["subject"]
        self._get_attachments_for_microsoft_mail(incoming_email=incoming_email, headers=headers)
        return {
            "from": self.sender,
            "date": self.date,
            "subject": self.subject,
            "body_preview": self.body_preview,
            "body": self.body,
            "attachments": self.attachments
        }


    def _get_attachments_for_microsoft_mail(self, incoming_email, headers):
        id = incoming_email["id"]
        endpoint = f"https://graph.microsoft.com/v1.0/me/messages/{id}/attachments"
        print(id)
        print(incoming_email['hasAttachments'])
        if 'hasAttachments' in incoming_email and incoming_email['hasAttachments'] is True:
            response = requests.get(endpoint,headers=headers)
            data = response.json()
            for attachment in data["value"]:
                print(attachment)
                content = attachment['contentBytes']
                decoded = base64.b64decode(content)
                decoded = decoded.decode()
                _attachment = {
                    "name":  attachment['name'],
                    "type": attachment["contentType"],
                    "data": decoded
                }
                self.attachments.append(_attachment)
                print(_attachment)


    def get_email_content_for_gmail(self):
        headers_message = self.email_service.users().messages().get(userId='me', id=self.id).execute()
        self._set_email(headers_message=headers_message)
        return {
            "from": self.sender,
            "date": self.date,
            "subject": self.subject,
            "body_preview": self.body_preview,
            "body": self.body,
            "attachments": self.attachments
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
        for part in parts:
            body_of_part = part["body"]
            if 'attachmentId' in body_of_part:
                print(part)
                self._get_attachment(part=part)
            else:
                soup = self._get_body_through_decoding(part=part)
            body = str(soup)
        return body


    def _get_attachment(self, part):
        payload_body = part["body"]
        data = payload_body["attachmentId"]
        headers_message = self.email_service.users().messages().attachments().get(userId='me', messageId=self.id,id=data).execute()
        data = headers_message["data"]
        data = data.replace("-","+").replace("_","/")
        decoded = base64.b64decode(data)
        decoded = decoded.decode()
        attachment = {
            "name":  part['filename'],
            "type": part["mimeType"],
            "data": decoded
        }
        self.attachments.append(attachment)


    def _get_body_through_decoding(self,part): 
        payload_body = part["body"]
        data = payload_body["data"]
        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode(data)
        soup = BeautifulSoup(decoded_data, "lxml")
        return str(soup.body)
