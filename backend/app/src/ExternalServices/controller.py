import json
import logging
from fastapi import Request, Response, status
from app.src.ErrorsAndExceptions.Exceptions.InputExceptions import NotValidEmailFormatException, EmailNotInSupportedDomainsException
from googleapiclient.http import HttpError
from app.src.ExternalServices.services import ExternalServicesService
from app.src.ErrorsAndExceptions.Errors.TodoErrors import ErrorResponse
from app.src.ErrorsAndExceptions.Errors.InputErrors import InvalidEmail, UnsupportedDomainError
class ExternalServicesController():
    def __init__(self, settings):
        self.settings = settings
        self.service = ExternalServicesService(settings=self.settings)
        pass


    async def login(self, request: Request):
        try:
            body = await request.json()
            email = body["email"]
            redirect_uri = await self.service.login(email=email, request=request)
            return Response(
                content=json.dumps({"redirect": redirect_uri}),
                status_code=status.HTTP_200_OK
            )
        except NotValidEmailFormatException as e:
            logging.error(e)
            return InvalidEmail(
                input_type="email",
                error_message="Invalid email, check for missing @.",
                endpoint={"path":f"/login", "method": "POST", "body": {"data": email}},
                status=status.HTTP_400_BAD_REQUEST
            ).get_error()
        except EmailNotInSupportedDomainsException as e:
            logging.error(e)
            return UnsupportedDomainError(
                input_type="email",
                error_message="The used domain is not part of our support. We support gmail and outlook only.",
                endpoint={"path":f"/login", "method": "POST", "body": {"data": email}},
                status=status.HTTP_400_BAD_REQUEST
            ).get_error()


    async def auth(self, request: Request):
        username = await self.service.auth(request=request)
        return username


    async def get_mails(self):
        try:
            messages = await self.service.get_mails()
            if messages.__len__() == 0:
                return Response(
                content=json.dumps({"mails": messages}),
                status_code=status.HTTP_204_NO_CONTENT
            )
            return Response(
                content=json.dumps({"mails": messages}),
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
        response = await self.service.send_email(body=body)
        return response