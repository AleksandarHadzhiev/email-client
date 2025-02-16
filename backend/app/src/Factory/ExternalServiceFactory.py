from fastapi import HTTPException, status
from app.src.Google.sso import Google
from app.src.Microsoft.sso import Microsoft


class ExternalServiceFactory():    
    def __init__(self, email: str, settings):
        self.email = email
        self.settings = settings
        self.supported_domains = {
            "@gmail.com": Google(settings=settings),
            "@outlook.com": Microsoft(settings=settings)
        }


    def get_external_service_based_on_domain(self):
        domains = list(self.supported_domains.keys())
        for domain in domains:
            if self.email.endswith(domain):
                return self.supported_domains[domain]
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Domain is not supported in the app",
                headers={
                    "X-Error": "Domain is not supported"
                }
            )
