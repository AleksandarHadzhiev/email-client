from app.src.Google.sso import Google
from app.src.Microsoft.sso import Microsoft
from app.src.ErrorsAndExceptions.Exceptions.InputExceptions import EmailNotInSupportedDomainsException

class ExternalServiceFactory():    
    def __init__(self, email: str, settings):
        self.email = email
        self.settings = settings
        self.supported_domains = {
            "@gmail.com": Google(settings=settings),
            "@outlook.com": Microsoft(settings=settings)
        }


    def get_external_service_if_in_supported_domain(self):
        domains = list(self.supported_domains.keys())
        for domain in domains:
            if self.email.endswith(domain):
                return self.supported_domains[domain]
        raise EmailNotInSupportedDomainsException(
                f"The provided email {self.email} is not part of the supported domains"
            )
