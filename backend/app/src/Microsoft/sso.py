import identity.web
import requests
from app.src.Microsoft.service import MicrosoftService
from app.src.modules.email import Email
from app.src.ExternalServices.external_service_provider import ExternalServiceProvider

class Microsoft(ExternalServiceProvider):
    def __init__(self, settings):
        super().__init__(settings)
        self.authority =f"https://login.microsoftonline.com/common"
        self.service = MicrosoftService()
        self.auth: identity.web.Auth = None
    
    
    async def login(self, data: dict = None, request = None):
        auth = identity.web.Auth(
            session=request.session,
            authority=self.authority,
            client_id=self.settings.MICROSOFT_CLIENT_ID,
            client_credential=self.settings.MICROSOFT_CLIENT_SECRET,
        )
        self.set_auth(auth=auth)
        response = auth.log_in(
            scopes=self.settings.MICROSOFT_SCOPE,
            redirect_uri=self.settings.REDIRECT_URI,
        )
        redirec_uri = f'{response["auth_uri"]}&login_hint={data["email"]}'
        return {"redirect_uri": redirec_uri}


    async def callback(self, request):
        body = await request.json()
        login_data = self.service.get_data_for_login(request_body=body)
        result = self.auth.complete_log_in(login_data)
        if "error" in result:
            raise result["error"]
        user = self.auth.get_user()
        return user["preferred_username"]


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
