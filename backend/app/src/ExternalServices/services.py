from fastapi import Request
from app.src.ExternalServices.external_service_provider import ExternalServiceProvider
from app.src.Factory.ExternalServiceFactory import ExternalServiceFactory
from app.src.ErrorsAndExceptions.Exceptions.InputExceptions import NotValidEmailFormatException

class ExternalServicesService():
    def __init__(self, settings):
        self.settings = settings


    def _get_external_service(self) -> ExternalServiceProvider:
        return self.external_service_provider


    def login(self, email: str,request: Request):
        email = self._get_email_if_valid_email_format(email=email)
        external_service = self._build_external_service(email=email)
        redirect_uri = external_service.login(email=email, request=request)
        return redirect_uri


    def _get_email_if_valid_email_format(self, email: str):
        if "@" not in email:
            raise NotValidEmailFormatException("The emal format is invalid.")
        return email


    def _build_external_service(self, email)  -> ExternalServiceProvider:
        factory = ExternalServiceFactory(settings=self.settings, email=email)
        external_service = factory.get_external_service_if_in_supported_domain()
        self._set_external_service(external_service=external_service)
        return external_service


    def _set_external_service(self, external_service: ExternalServiceProvider):
        self.external_service_provider = external_service


    def auth(self, request: Request):
        external_service = self._get_external_service()
        username = external_service.callback(request=request)
        return username


    def get_mails(self):
        external_service = self._get_external_service()
        mails = external_service.get_emails()
        return mails


    async def send_email(self, body):
        external_service = self._get_external_service()
        response = await external_service.send_email(data=body)
        return response


    async def get_mail_by_id(self, id:str):
        external_service = self._get_external_service()
        email = external_service.get_email_by_id(id=id)
        return email
