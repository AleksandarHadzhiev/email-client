import json
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response, status
from sqlmodel import Session
from app.db import DBConnector
from app.settings import Settings
from app.src.Todos.service import ToDoService
from app.src.Errors.JSONDecodeErrorResponse import JSONDecodeErrorResponse
from app.src.Errors.TodoErrors import ErrorResponse

db = DBConnector()
SessionDep = Annotated[Session, Depends(db.get_session)]

class TodoController():
    
    def __init__(self, settings:Settings):
        self.settings = settings
        self.service = ToDoService(settings=settings)


    async def create(self, request: Request, session: SessionDep):
        try:
            body = await request.json()
            todo = self.service.create_todo(body=body, session=session)
            return Response(content=json.dumps(todo.get_formatted()), status_code=status.HTTP_201_CREATED)
        except (json.JSONDecodeError) as e:
            logging.error(e)
            return JSONDecodeErrorResponse(msg=e.msg, endpoint= {"path":'/todos', "method": "POST"}).response()
        except HTTPException as e:
            logging.exception(e)
            return ErrorResponse(detail=e.detail, endpoint= {"path":'/todos', "method": "POST"}, status=e.status_code).response()


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
            todo = self.service.edit_todo(body=body, id=id, session=session)
            return Response(content=json.dumps(todo.get_formatted()), status_code=status.HTTP_200_OK)
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

