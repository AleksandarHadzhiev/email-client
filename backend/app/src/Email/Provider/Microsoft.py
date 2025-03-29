import identity.web
import requests
from app.src.modules.email import Email
from app.src.Email.email_provider import EmailProvider


class Microsoft(EmailProvider):
    def __init__(self, settings):
        super().__init__(settings)
        self.authority =f"https://login.microsoftonline.com/common"
    

    async def get_emails(self):
        token = self.auth.get_token_for_user(self.settings.MICROSOFT_SCOPE)
        endpoint = "https://graph.microsoft.com/v1.0/me/messages"
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        response = requests.get(endpoint,headers=headers)
        emails = response.json()
        parsed_emails = []
        for email in emails["value"]:
            mail: Email = Email(id = email["id"], email_service=None)
            parsed_email = mail.get_email_content_for_microsoft(incoming_email=email, headers=headers)
            parsed_emails.append(parsed_email)
        return parsed_emails


    async def send_email(self, data):
        token = self.auth.get_token_for_user(self.settings.MICROSOFT_SCOPE)
        endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
        headers = {"Authorization": f"Bearer {token['access_token']}", "Content-Type": "application/json"}
        email_body = self.service.generate_email_body(body=data)
        response = requests.post(endpoint,headers=headers,json=email_body)
        if response.status_code == 202:
            return {"status": 'SENT'}
        else:
            return {"fail": response.text}


    def get_email_by_id(self, id):
        return super().get_email_by_id(id)
