import json
import logging
from fastapi import Request, Response, status
from app.src.Login.service import LoginService
from app.src.ErrorsAndExceptions.Errors.InputErrors import InputError
from app.src.DTOs.DTOFactory import DTOFactory
from app.src.DTOs.login_dto import BaseDTO
from app.src.validations.csrf_protector import CSRFProtector

class LoginController():
    def __init__(self, settings):
        self.settings = settings
        self.service = LoginService(settings=self.settings)
        self.csrf = CSRFProtector()
        pass


    async def login(self, request: Request):
        body = await request.json()
        endpoint={
            "path": "/login",
            "method":"POST",
            "body": body
        }
        is_not_authorized = self._check_for_authorized_access(request=request, endpoint=endpoint)
        if is_not_authorized is not None:
            return is_not_authorized.as_response()
        # try:
        factory = DTOFactory(data=body)
        loginDTO: BaseDTO = factory.get_dto_based_on_incoming_data()
        response = await self.service.login(dto=loginDTO, request=request)
        logging.info(response)
        new_token = self.csrf.provide_ative_token()
        response["csrf"] = new_token["token"]
        return self._handle_basic_response(response=response, _endpoint=endpoint, success_code=status.HTTP_200_OK)


    def _check_for_authorized_access(self, request: Request, endpoint):
        token = request.headers.get('csrf')
        if token is None:
            return InputError(
                input=endpoint["body"],
                error_message="Unauthorized access!",
                status=status.HTTP_401_UNAUTHORIZED,
                endpoint=endpoint
            )
        is_authorized = self.csrf.compare_token(token=token)
        if is_authorized is False:
            return InputError(
                input=endpoint["body"],
                error_message="Unauthorized access!",
                status=status.HTTP_401_UNAUTHORIZED,
                endpoint=endpoint
            )
        return None

    def _handle_basic_response(self,response: dict, _endpoint: dict, success_code: status) -> Response:
        if "fail" in response:
            logging.error(response["fail"])
            return InputError(
                input=_endpoint["body"],
                error_message=response,
                status=status.HTTP_400_BAD_REQUEST,
                endpoint=_endpoint,
            ).as_response()
        print(response)
        return Response(
            content=json.dumps(response),
            status_code=success_code
        )


    async def auth(self, request: Request):
        try:
            body = await request.json()
            _endpoint={
                "path": "/auth",
                "method":"POST",
                "body": body
            }
            is_not_authorized = self._check_for_authorized_access(request=request, endpoint=_endpoint)
            if is_not_authorized is not None:
                return is_not_authorized.as_response()
            response = await self.service.auth(request=request)
            new_token = self.csrf.provide_ative_token()
            response["csrf"] = new_token["token"]
            print(response)
            return self._handle_basic_response(response=response, _endpoint=_endpoint, success_code=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
