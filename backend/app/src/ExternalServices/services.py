from fastapi import HTTPException, Request, status
from app.src.ExternalServices.external_service_provider import ExternalServiceProvider
from app.src.Factory.ExternalServiceFactory import ExternalServiceFactory


class ExternalServicesService():
    def __init__(self, settings):
        self.settings = settings


    def _get_external_service(self) -> ExternalServiceProvider:
        return self.external_service_provider


    def login(self, email: str,request: Request):
        email = self._validate_email(email=email)
        external_service = self._build_external_service(email=email)
        redirect_uri = external_service.login(email=email, request=request)
        return redirect_uri


    def _validate_email(self, email: str):
        if "@" not in email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email",
                headers={
                    "X-Error": "Invalid email"
                }
            )
        return email


    def _build_external_service(self, email)  -> ExternalServiceProvider:
        factory = ExternalServiceFactory(settings=self.settings, email=email)
        external_service = factory.get_external_service_based_on_domain()
        if external_service is None:
            print(external_service)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Domain is not supported in the app",
                headers={
                    "X-Error": "Domain is not supported"
                }
            )
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


    async def get_mail_by_id(self, id:int):
        external_service = self._get_external_service()
        email = external_service.get_email_by_id(id=id)
        return email
