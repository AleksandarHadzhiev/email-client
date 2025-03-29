from app.src.Email.Provider.Google import Google
from app.src.Email.Provider.Microsoft import Microsoft

class EmailProviderFactory():    
    def __init__(self, sso_provider: str, settings):
        self.sso_provider = sso_provider
        self.allowed_email_providers = {
            "google": Google(settings=settings),
            "microsoft": Microsoft(settings=settings)
        }


    def get_email_provider(self):
        providers = list(self.allowed_email_providers.keys())
        for provider in providers:
            print(type(provider))
            print(type(self.sso_provider))
            if provider == self.sso_provider:
                return {"provide": self.allowed_email_providers[provider]}
        return {
            "fail": "The provider is not supported."
        }