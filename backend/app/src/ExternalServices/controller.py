import json
import logging
from fastapi import Request, Response, status
from fastapi.exceptions import HTTPException
from app.src.ExternalServices.services import ExternalServicesService
from app.src.Errors.TodoErrors import ErrorResponse

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
        except HTTPException as e:
            logging.error(e)
            return ErrorResponse(
                detail=  e.detail,
                endpoint={"path":f"/login/{email}", "method": "POST"},
                status=e.status_code
            ).response()



    async def auth(self, request: Request):
        username = await self.service.auth(request=request)
        return username


    async def get_mails(self):
        messages = await self.service.get_mails()
        return messages


    async def get_mail(self, id:int):
        email = await self.service.get_mail_by_id(id=id)
        return email


    async def send_message(self, request: Request):
        body = await request.json()
        response = await self.service.send_email(body=body)
        return response