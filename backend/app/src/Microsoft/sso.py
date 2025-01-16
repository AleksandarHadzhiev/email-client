import identity.web
from app.settings import Settings
from fastapi import  Request
from app.src.Microsoft.service import MicrosoftService

class MicrosoftSSO():
    
    def __init__(self, settings: Settings):
        self.authority =f"https://login.microsoftonline.com/common"
        self.settings = settings
        self.service = MicrosoftService()


    def set_auth(self, auth):
        self.auth = auth


    async def login(self, request: Request, email: str):
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
        redirec_uri = f'{response["auth_uri"]}&login_hint={email}'  
        return redirec_uri

    async def logout(self):
        return self.auth.log_out(self.settings.FRONTEND_URL)


    async def callback(self, request: Request):
        body = request
        login_data = self.service.get_data_for_login(request_body=body)
        result = self.auth.complete_log_in(login_data)
        user = self.auth.get_user()
        return user["preferred_username"]
        