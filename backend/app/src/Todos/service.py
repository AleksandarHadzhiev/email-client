from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from app.db import DBConnector
from app.src.modules.todo_model import TodoModel
from app.src.validations.validation_factory import ValidationFactory
from app.src.DTOs.base import BaseDTO

db = DBConnector()
SessionDep = Annotated[Session, Depends(db.get_session)]


class ToDoService():
    
    def __init__(self, settings):
        self.settings = settings


    def create_todo(self, body: BaseDTO, session):
        factory = ValidationFactory(incoming_data=body)
        validation = factory.get_the_needed_type_of_validation()
        dict_format = body.get_values_as_dict()
        response = validation.get_data_if_valid(data=dict_format)
        if "fail" in response:
            return response
        todo = TodoModel(
            email=dict_format["email"],
            title=dict_format["title"],
            description=self._get_todo_description(body=dict_format),
            due_date=self._get_todo_due_date(body=dict_format),
        )
        return self._store_todo_in_db(session=session, todo=todo)


    def _input_validation(self, body):
        if 'email' not in body or body["email"] == "":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing email",
                headers={
                    "X-Error": "No email provided"
                }
            )
        self._validate_title(body=body)
        self._validate_email(email=body["email"])


    def _validate_title(self, body):
        if 'title' not in body or body["title"] == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing title",
                headers={
                    "X-Error": "No title provided"
                }
            )

    def _validate_email(self, email: str):
        if email.isspace() or email.__len__() == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing email",
                headers={
                    "X-Error": "No email provided"
                }
            )
        elif email.endswith("@gmail.com") == False and email.endswith("@outlook.com") == False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email domain not supported",
                headers={
                    "X-Error": "Email domain not supported"
                }
            )


    def _get_todo_description(self, body):
        if 'description' in body:
            return body["description"]
        return ""


    def _get_todo_due_date(self, body):
        if 'date' in body:
            return body["date"]
        return ""


    def _store_todo_in_db(self, session, todo):
        try:
            session.add(todo)
            session.commit()
            session.refresh(todo)
            if todo.id != None:
                return {"message": "Added task to your list"}
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DB related error, try again with new data.",
                headers={
                    "X-Error": "DB related error"
                }
            )


    def get_todos_for_email(self, email, session: SessionDep):
        self._validate_email(email=email)
        todos = session.exec(select(TodoModel).where(TodoModel.email == email.strip())).all()
        _formated = []
        for todo in todos:
            _formated.append(self._get_todo_in_dict_format(todo=todo))
        return _formated


    def _get_todo_in_dict_format(self, todo: TodoModel):
        return {
            "email": todo.email,
            "title": todo.title,
            "desc": todo.description,
            "due": todo.due_date,
            "id": todo.id
        }


    def get_todo_by_id(self, id, session: SessionDep):
        todo = session.get(TodoModel, id)
        if not todo:
            raise HTTPException(status_code=404, detail="ToDo not found")
        return todo


    def delete(self, id, session: SessionDep):
        todo = self.get_todo_by_id(id=id, session=session)
        session.delete(todo)
        session.commit()


    def edit_todo(self, id:int, body: BaseDTO, session: SessionDep):
        todo = self.get_todo_by_id(id=id, session=session)
        factory = ValidationFactory(incoming_data=body)
        validation = factory.get_the_needed_type_of_validation()
        dict_format = body.get_values_as_dict()
        response = validation.get_data_if_valid(data=dict_format)
        if "fail" in response:
            return response
        todo.title=dict_format["title"]
        todo.description=self._get_todo_description(body=dict_format)
        todo.due_date=self._get_todo_due_date(body=dict_format)
        session.commit()
        session.refresh(todo)
        return {"message": "Editted task to your list"}
