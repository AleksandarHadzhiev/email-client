from fastapi import Request
from app.settings import Settings
from app.src.Login.SSO.SSO_provider import SSOProvider
from app.src.Factory.ExternalServiceFactory import ExternalServiceFactory
from app.src.DTOs.login_dto import BaseDTO

class LoginService():
    def __init__(self, settings: Settings):
        self.settings = settings


    def _get_external_service(self) -> SSOProvider:
        return self.external_service_provider


    def _set_external_service(self, external_service: SSOProvider):
        self.external_service_provider = external_service


    async def login(self, dto: BaseDTO,request: Request):
        dict = dto.get_values_as_dict()
        external_service_dict =  await self._build_external_service(dto=dto)
        if "fail" in external_service_dict:
            return external_service_dict
        sso: SSOProvider = external_service_dict["domain"]
        self._set_external_service(external_service=sso)
        response = await sso.login(data=dict, request=request)
        return response


    async def _build_external_service(self, dto: BaseDTO) -> dict:
        factory = ExternalServiceFactory(settings=self.settings, external_service_login=dto)
        external_service_dict = factory.get_external_service_if_in_supported_domain()
        return external_service_dict


    async def auth(self, request: Request):
        external_service = self._get_external_service()
        response = await external_service.auth(request=request)
        return response