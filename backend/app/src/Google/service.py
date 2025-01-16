import requests

from urllib import parse
from app.settings import Settings


class GoogleService():
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.token_url = "https://accounts.google.com/o/oauth2/token"
    
    
    def get_google_provider_cfg(self):
        return requests.get(self.settings.DISCOVERY_URL).json()


    def get_code_from_redirect_url(self, request_body):
        pathname = request_body["pathname"]
        parsed_url = parse.urlparse(pathname)
        code = parse.parse_qs(parsed_url.query)["code"][0]
        return code
    
    
    def generate_access_token(self, code):
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        
        response = requests.post(self.token_url, data=data)
        access_token = response.json().get("access_token")
        return access_token
    
    
    def get_user_info(self, access_token):
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        return user_info
