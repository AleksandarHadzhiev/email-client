from app.src.Google.sso import Google
from app.src.Microsoft.sso import Microsoft
from app.src.validations.base_validation import BaseValidation
from app.src.validations.validation_factory import ValidationFactory
from app.src.DTOs.login_dto import ExternalServiceLogin
from app.src.ABV.ABVExternalServiceProvider import ABV

class ExternalServiceFactory():    
    def __init__(self, external_service_login: ExternalServiceLogin, settings):
        self.external_service_login = external_service_login
        self.settings = settings
        self.supported_domains = {
            "@gmail.com": Google(settings=settings),
            "@outlook.com": Microsoft(settings=settings),
            "@abv.bg": ABV(settings=settings),
        }


    def get_external_service_if_in_supported_domain(self):
        factory = ValidationFactory(incoming_data= self.external_service_login)
        email = self.external_service_login.email
        validation_checker = factory.get_the_needed_type_of_validation()
        if issubclass(type(validation_checker), BaseValidation) == False:
            return validation_checker
        validation_response = validation_checker.get_data_if_valid(data=self.external_service_login.get_values_as_dict())
        if "fail" in validation_response:
            return validation_response
        
        domains = list(self.supported_domains.keys())
        for domain in domains:
            if email.endswith(domain):
                return {"domain": self.supported_domains[domain]}
        return {
            "fail": f"the provided email: {email} is not part of the supported domains: {domains}"
        }
