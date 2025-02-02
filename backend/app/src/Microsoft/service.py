import base64
from urllib.parse import parse_qs, urlparse
from werkzeug.datastructures import ImmutableMultiDict

class MicrosoftService():
    
    def __init__(self):
        pass
    
    def get_data_for_login(self, request_body):
        pathname = request_body["pathname"]
        parse_res = urlparse(pathname)
        query_params = parse_qs(parse_res.query)
        login_data = ImmutableMultiDict(
            [
                ('code', query_params["code"][0]),
                ('client_info', query_params["client_info"][0]),
                ('state', query_params["state"][0]),
            ]
        )
        
        return login_data


    def generate_email_body(self,body):
        email_body = {
                "message": {
                    "subject": body["subject"],
                    "body": {
                        "contentType": "text",
                        "content": body["body"]
                        },
                    "toRecipients": [
                        {
                            "emailAddress": {
                            "address":  body["to"]
                            }
                        }
                    ]
                },
            "saveToSentItems": "true"
            }
        if 'attachments' in body:
            email_body = self._attach_attachments(email_body=email_body, body=body)
        return email_body


    def _attach_attachments(self, email_body, body):
        email_body["message"]["attachments"] = []
        attachments = body['attachments']            
        for attachment in attachments:
            attachment_to_add = {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "Name": attachment["name"],
                "contentType": attachment["type"],
                "ContentBytes": self._generate_content_bytes(attachment=attachment)
            }
            email_body["message"]["attachments"].append(attachment_to_add)
        return email_body


    def _generate_content_bytes(self, attachment):
        content = attachment["content"]
        encoded = str(base64.b64encode(content.encode()))
        encoded = encoded.replace("b'", '')
        encoded = encoded.replace("'", '')
        return encoded
