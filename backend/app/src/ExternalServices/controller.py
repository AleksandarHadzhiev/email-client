import json
import logging
from fastapi import Request, Response, status
from googleapiclient.http import HttpError
from app.src.ExternalServices.services import ExternalServicesService
from app.src.ErrorsAndExceptions.Errors.TodoErrors import ErrorResponse
from app.src.ErrorsAndExceptions.Errors.InputErrors import InputError
from app.src.DTOs.DTOFactory import DTOFactory
from app.src.DTOs.login_dto import BaseDTO
from app.src.validations.csrf_protector import CSRFProtector

class ExternalServicesController():
    def __init__(self, settings):
        self.settings = settings
        self.service = ExternalServicesService(settings=self.settings)
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
        # except Exception as e:
        #     logging.error(e)
        #     return Error(
        #         detail=str(e),
        #         endpoint={"path":f"/login", "method": "POST", "body": body},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     ).as_response()


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
            return self._handle_basic_response(response=response, _endpoint=_endpoint, success_code=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)


    async def get_mails(self, request: Request):
        try:
            _endpoint={
                "path": "/get/mails",
                "method":"GET",
                "body": []
            }
            is_not_authorized = self._check_for_authorized_access(request=request, endpoint=_endpoint)
            if is_not_authorized is not None:
                return is_not_authorized.as_response()
            messages = await self.service.get_mails()
            new_token = self.csrf.provide_ative_token()
            if messages.__len__() == 0:
                return Response(
                content=json.dumps({"mails": messages, "csrf": new_token["token"]}),
                status_code=status.HTTP_204_NO_CONTENT
            )
            return Response(
                content=json.dumps({"mails": messages, "csrf": new_token["token"]}),
                status_code=status.HTTP_200_OK
            )
        except HttpError as e:
            logging(e.response.reason)
            return ErrorResponse(
                detail=  e.response.reason,
                endpoint={"path":f"/mails", "method": "GET"},
                status=e.response.status_code
            ).response()


    async def get_mail(self, id:str):
        try:
            email = await self.service.get_mail_by_id(id=id)
            if email != None:
                return Response(
                content=json.dumps({"email": email}),
                status_code=status.HTTP_200_OK
            )
            return Response(
                content=json.dumps({"email": {}}),
                status_code=status.HTTP_204_NO_CONTENT)
        except HttpError as e:
            logging.error(e)
            return ErrorResponse(
                detail=  {id: e.reason},
                endpoint={"path":f"/mail/{id}", "method": "GET"},
                status=e.status_code
            ).response()


    async def send_message(self, request: Request):
        body = await request.json()
        try:
            _endpoint={
                "path": "/send",
                "method":"POST",
                "body": body
            }
            is_not_authorized = self._check_for_authorized_access(request=request, endpoint=_endpoint)
            if is_not_authorized is not None:
                return is_not_authorized.as_response()
            factory = DTOFactory(data=body)
            email_object_dto = factory.get_dto_based_on_incoming_data()
            if issubclass(type(email_object_dto),BaseDTO) == False:
                logging.error(email_object_dto)
                return ErrorResponse(
                    detail=  email_object_dto["fail"],
                    endpoint={"path":f"/send", "method": "POST", "body": body},
                    status=status.HTTP_400_BAD_REQUEST
                ).response()
            response = await self.service.send_email(body=email_object_dto)
            new_token = self.csrf.provide_ative_token()
            response["csrf"] = new_token["token"]
            # Do some sort of check
            # It should return different thing and not just SENT
            return self._handle_basic_response(response=response, _endpoint=_endpoint, success_code=status.HTTP_201_CREATED)
        except HttpError as e:
            logging.error(e)
            return ErrorResponse(
                detail=  {id: e.reason},
                endpoint={"path":f"/send", "method": "POST", "body": body},
                status=e.status_code
            ).response()