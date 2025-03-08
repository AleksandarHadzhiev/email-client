import base64
import email
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import quopri
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
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
        if 'attachments' in body:
            message = self._attach_attachments(body=body)
        else:
            message = self._message_without_attachments(body=body)
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}  


    def _attach_attachments(self, body):
        attachments = body['attachments']
        message = MIMEMultipart()
        self._set_basic_info(message=message, body=body)
        message.attach(MIMEText(body["body"]))
        for attachment in attachments:
            self._generate_attachment(attachment=attachment, message=message)
        return message


    def _set_basic_info(self, message, body):
        message['To'] = body["to"]
        message['From'] = body["from"]
        message['Subject'] = body["subject"]


    def _generate_attachment(self, attachment, message):
        main_type, sub_type = attachment["type"].split('/', 1)
        content = attachment["content"]
        if main_type == 'text':
            msg = MIMEText(content, _subtype =sub_type)
        elif main_type == "image":
            content = str(content).encode() 
            msg = MIMEImage(content, _subtype =sub_type)
        msg.add_header('Content-Disposition', 'attachment', filename=attachment["name"])
        message.attach(msg)


    def _message_without_attachments(self, body):
        message = MIMEText(body["body"])
        self._set_basic_info(message=message, body=body)
        return message


    def get_email_content_for_microsoft(self, incoming_email, headers):
        body = incoming_email["body"]["content"]
        soup = BeautifulSoup(body, "lxml")
        self._set_email_information(soup=soup, incoming_email=incoming_email)
        self._check_if_email_has_attachments(incoming_email=incoming_email, headers=headers)
        return {
            "from": self.sender,
            "date": self.date,
            "subject": self.subject,
            "body_preview": self.body_preview,
            "body": self.body,
            "attachments": self.attachments
        }


    def _set_email_information(self, soup, incoming_email):
        self.body = str(soup.body)
        self.body_preview = incoming_email["bodyPreview"]
        self.date = incoming_email["receivedDateTime"]
        self.sender = incoming_email["sender"]["emailAddress"]["name"] + "<" + incoming_email["sender"]["emailAddress"]["address"] + ">"
        self.subject = incoming_email["subject"]


    def _check_if_email_has_attachments(self, incoming_email, headers):
        id = incoming_email["id"]
        endpoint = f"https://graph.microsoft.com/v1.0/me/messages/{id}/attachments"
        if 'hasAttachments' in incoming_email and incoming_email['hasAttachments'] is True:
            self._set_attachments(endpoint=endpoint, headers=headers)


    def _set_attachments(self, endpoint, headers):
        response = requests.get(endpoint,headers=headers)
        data = response.json()
        for attachment in data["value"]:
            content = attachment['contentBytes']
            decoded = base64.b64decode(content)
            decoded = decoded.decode()
            _attachment = {
                "name":  attachment['name'],
                "type": attachment["contentType"],
                "data": decoded
            }
            self.attachments.append(_attachment)


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


    def get_email_content_for_pop3(self, emails: list[bytes], messages: list):
        times = 0
        elements = []
        for msg in emails:
            body_element = msg.decode()
            elements = self._get_body_content(msg=msg, elements=elements)
            if "Content-Transfer-Encoding" in body_element:
                times+=1
                if times == 2:
                    elements.clear()
            self._set_abv_mail_headers(msg=msg)
        message = self._form_email(elements=elements)
        messages.append(message)
        return messages


    def _set_abv_mail_headers(self, msg):
        mail = email.message_from_bytes(msg)
        keys = mail.keys()
        self._get_sender(keys, mail)
        if "Date" in keys:
            self.date = mail['Date']
        self._get_subject(keys, mail)


    def _get_body_content(self, msg: bytes, elements: list):
        if msg.decode() is not None:
            body_element = msg.decode()
            if "Part" not in body_element and "--=" not in body_element and "-- =" not in body_element:
                if body_element.endswith("="):
                    body_element = body_element.removesuffix("=")
                elements.append(body_element)
        return elements


    def _get_sender(self, keys, mail):
        sender = ""
        if 'From' in keys:
            email_address=""
            sender = str(mail['From'])
            if "=?UTF-8?B?" in mail["From"]:
                _email = str(sender).split('<', 1)
                email_address = f"<{_email[1]}"
                sender = sender.replace("=?UTF-8?B?", "")
                sender = base64.b64decode(sender).decode()
            else:
                sender = mail['From']
            self.sender = f"{sender} {email_address}"


    def _get_subject(self, keys, mail):
        subject = ""
        if 'Subject' in keys:
            subject = str(mail['Subject'])
            if "=?UTF-8?B?" in mail["Subject"]:
                subject = subject.replace("=?UTF-8?B?", "")
                subject = base64.b64decode(subject).decode()
            elif "=?utf-8?Q?" in mail["Subject"]:
                subject = subject.replace("=?utf-8?Q?", "")  
                subject = quopri.decodestring(subject).decode()
            self.subject = subject


    def _form_email(self, elements):

        try:
            joined_str = quopri.decodestring("".join(elements)).decode(errors="ignore")
        except:
            joined_str = "".join(elements)
        body = joined_str
        message = {
            "from": self.sender,
            "date": self.date,
            "subject": self.subject,
            "body_preview": "Something",
            "body": body,
            "attachments": []
        }
        return message
