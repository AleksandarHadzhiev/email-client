import json
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response, status
from sqlmodel import Session
from app.db import DBConnector
from app.settings import Settings
from app.src.Todos.service import ToDoService
from app.src.ErrorsAndExceptions.Errors.JSONDecodeErrorResponse import JSONDecodeErrorResponse
from app.src.ErrorsAndExceptions.Errors.TodoErrors import ErrorResponse
from app.src.DTOs.base import BaseDTO
from app.src.DTOs.DTOFactory import DTOFactory
from app.src.ErrorsAndExceptions.Errors.InputErrors import InputError

db = DBConnector()
SessionDep = Annotated[Session, Depends(db.get_session)]

class TodoController():
    
    def __init__(self, settings:Settings):
        self.settings = settings
        self.service = ToDoService(settings=settings)


    async def create(self, request: Request, session: SessionDep):
        body = await request.json()
        try:
            factory = DTOFactory(data=body)
            endpoint= {"path":'/todos', "method": "POST", "body": body}
            create_todo: BaseDTO = factory.get_dto_based_on_incoming_data()
            response = self.service.create_todo(body=create_todo, session=session)
            return self._handle_basic_response(response=response, _endpoint=endpoint, success_code=status.HTTP_201_CREATED)
        except (json.JSONDecodeError) as e:
            logging.error(e)
            return JSONDecodeErrorResponse(msg=e.msg, endpoint= {"path":'/todos', "method": "POST"}).response()
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":'/todos', "method": "POST"}, status=e.status_code).response()

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


    async def get_todos(self, email: str, session: SessionDep):
        try:
            todos = self.service.get_todos_for_email(email=email, session=session)
            if todos.__len__() == 0:
                return Response(content=json.dumps({"email": email.strip(), "todos":[]}),status_code=status.HTTP_204_NO_CONTENT)
            return Response(content=json.dumps({"email": email.strip(), "todos": todos}), media_type="json", status_code=status.HTTP_200_OK)
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{email}', "method": "GET"}, status=e.status_code).response()


    async def edit(self, request: Request, id: int, session: SessionDep):
        try:
            body = await request.json()
            factory = DTOFactory(data=body)
            endpoint= {"path":'/todos', "method": "POST", "body": body}
            create_todo: BaseDTO = factory.get_dto_based_on_incoming_data()
            response = self.service.edit_todo(body=create_todo, id=id, session=session)
            return self._handle_basic_response(response=response, _endpoint=endpoint, success_code=status.HTTP_200_OK)
        except (json.JSONDecodeError) as e:
            logging.error(e)
            return JSONDecodeErrorResponse(msg=e.msg, endpoint= {"path":f'/todos/{id}', "method": "PUT"}).response()
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{id}', "method": "PUT"}, status=e.status_code).response()


    async def get_todo(self, id: int, session: SessionDep):
        try:
            todo = self.service.get_todo_by_id(id=id, session=session)
            return Response(content=json.dumps(todo.get_formatted()), status_code=status.HTTP_200_OK)
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{id}', "method": "GET"}, status=e.status_code).response()



    async def delete(self, id: int, session: SessionDep):
        try:
            self.service.delete(id=id, session=session)
            return Response(status_code=status.HTTP_200_OK)
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{id}', "method": "DELETE"}, status=e.status_code).response()

