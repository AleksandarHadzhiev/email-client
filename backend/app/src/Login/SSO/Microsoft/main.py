import identity.web
from app.src.Login.SSO.Microsoft.service import MicrosoftService
from app.src.Login.SSO.SSO_provider import SSOProvider

class MicrosoftProvider(SSOProvider):
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


    async def auth(self, request):
        body = await request.json()
        login_data = self.service.get_data_for_login(request_body=body)
        result = self.auth.complete_log_in(login_data)
        if "error" in result:
            raise result["error"]
        user = self.auth.get_user()
        return {"email": user["preferred_username"], "type": "microsoft"}
