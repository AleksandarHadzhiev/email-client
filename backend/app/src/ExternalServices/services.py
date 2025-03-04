import poplib
from fastapi import Request
from app.settings import Settings
from app.src.ExternalServices.external_service_provider import ExternalServiceProvider
from app.src.Factory.ExternalServiceFactory import ExternalServiceFactory
from app.src.DTOs.login_dto import BaseDTO
from app.src.validations.base_validation import BaseValidation
from urllib.parse import parse_qs, urlparse
from app.src.validations.validation_factory import ValidationFactory


class ExternalServicesService():
    def __init__(self, settings: Settings):
        self.settings = settings


    def _get_external_service(self) -> ExternalServiceProvider:
        return self.external_service_provider


    def _set_mailbox(self, mailbox: poplib.POP3_SSL):
        self.mailbox = mailbox


    def _get_mailbox(self) -> poplib.POP3_SSL:
        return self.mailbox


    async def login(self, dto: BaseDTO,request: Request):
        dict = dto.get_values_as_dict()
        external_service_dict =  await self._build_external_service(dto=dto)
        if "fail" in external_service_dict:
            return external_service_dict
        external_service: ExternalServiceProvider = external_service_dict["domain"]
        self._set_external_service(external_service=external_service)
        response = await external_service.login(data=dict, request=request)
        return response


    async def _build_external_service(self, dto: BaseDTO) -> dict:
        print(f"DTO: {dto}")
        factory = ExternalServiceFactory(settings=self.settings, external_service_login=dto)
        external_service_dict = factory.get_external_service_if_in_supported_domain()
        return external_service_dict


    def _set_external_service(self, external_service: ExternalServiceProvider):
        self.external_service_provider = external_service


    async def auth(self, request: Request):
        external_service = self._get_external_service()
        response = await external_service.callback(request=request)
        print(f"RESPONSE AUTH: {response}")
        return response
        

    def get_mails(self):
        external_service = self._get_external_service()
        mails = external_service.get_emails()
        return mails


    async def send_email(self, body: BaseDTO):
        print(body)
        factory = ValidationFactory(incoming_data=body)
        email_object_validation = factory.get_the_needed_type_of_validation()
        if issubclass(type(email_object_validation), BaseValidation) == False:
            return email_object_validation
        print(type(email_object_validation))
        response = email_object_validation.get_data_if_valid(data=body.get_values_as_dict())
        if "fail" in response:
            return response
        external_service = self._get_external_service()
        response = await external_service.send_email(data=body.get_values_as_dict())
        return response


    async def get_mail_by_id(self, id:str):
        external_service = self._get_external_service()
        email = external_service.get_email_by_id(id=id)
        return email
