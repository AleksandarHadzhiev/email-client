import json
import logging
from fastapi import HTTPException, Request, Response, status
from app.settings import Settings
from app.db.DBConnector import DBConnector
from app.src.Todos.service import ToDoService
from app.src.ErrorsAndExceptions.Errors.JSONDecodeErrorResponse import JSONDecodeErrorResponse
from app.src.ErrorsAndExceptions.Errors.TodoErrors import ErrorResponse
from app.src.DTOs.base import BaseDTO
from app.src.DTOs.DTOFactory import DTOFactory
from app.src.ErrorsAndExceptions.Errors.InputErrors import InputError


class TodoController():
    
    def __init__(self, settings:Settings, db: DBConnector):
        self.settings = settings
        self.db = db.get_db()
        self.service = ToDoService(settings=settings)


    async def create(self, request: Request):
        body = await request.json()
        try:
            factory = DTOFactory(data=body)
            endpoint= {"path":'/todos', "method": "POST", "body": body}
            create_todo: BaseDTO = factory.get_dto_based_on_incoming_data()
            response = self.service.create_todo(body=create_todo, session=self.db)
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


    async def get_todos(self, email: str):
        try:
            todos = self.service.get_todos_for_email(email=email, session=self.db)
            if todos.__len__() == 0:
                return Response(content=json.dumps({"email": email.strip(), "todos":[]}),status_code=status.HTTP_204_NO_CONTENT)
            return Response(content=json.dumps({"email": email.strip(), "todos": todos}), media_type="json", status_code=status.HTTP_200_OK)
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{email}', "method": "GET"}, status=e.status_code).response()


    async def edit(self, request: Request, id: int):
        try:
            body = await request.json()
            factory = DTOFactory(data=body)
            endpoint= {"path":'/todos', "method": "POST", "body": body}
            create_todo: BaseDTO = factory.get_dto_based_on_incoming_data()
            response = self.service.edit_todo(body=create_todo, id=id, session=self.db)
            return self._handle_basic_response(response=response, _endpoint=endpoint, success_code=status.HTTP_200_OK)
        except (json.JSONDecodeError) as e:
            logging.error(e)
            return JSONDecodeErrorResponse(msg=e.msg, endpoint= {"path":f'/todos/{id}', "method": "PUT"}).response()
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{id}', "method": "PUT"}, status=e.status_code).response()


    async def get_todo(self, id: int):
        try:
            todo = self.service.get_todo_by_id(id=id, session=self.db)
            return Response(content=json.dumps(todo.get_formatted()), status_code=status.HTTP_200_OK)
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{id}', "method": "GET"}, status=e.status_code).response()



    async def delete(self, id: int):
        try:
            self.service.delete(id=id, session=self.db)
            return Response(status_code=status.HTTP_200_OK)
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":f'/todos/{id}', "method": "DELETE"}, status=e.status_code).response()

