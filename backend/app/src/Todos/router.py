import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session, select
from app.db import DBConnector
from app.settings import Settings
from app.src.modules.todo_model import TodoModel
from app.src.Todos.service import ToDoService

db = DBConnector()
SessionDep = Annotated[Session, Depends(db.get_session)]

ONLY_TITLE_PROVIDED = 2 # Will be changed to one

class TodoRouter():
    
    def __init__(self, settings:Settings):
        
        self.settings = settings
        self.router = APIRouter()
        self.service = ToDoService(settings=settings)
        self.router.add_api_route("/todo", self.create, methods=["POST"])
        self.router.add_api_route("/todos/{email}", self.get_todos, methods=["GET"])
        self.router.add_api_route("/todo/{id}", self.edit, methods=["PUT"])
        self.router.add_api_route("/todo/{id}", self.get_todo, methods=["GET"])
        self.router.add_api_route("/todo/{id}", self.delete, methods=["DELETE"])


    async def create(self, request: Request, session: SessionDep):
        body = await request.json()
        number_of_fields = len(body)
        if number_of_fields == ONLY_TITLE_PROVIDED: 
            todo = TodoModel(
                email=body["email"], # Will be changed to email from url
                title=body["title"]
            )
        else:
            todo = TodoModel(
                email=body["email"],
                title=body["title"],
                description=body["description"],
                due_date=body["due_date"],
            )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return "Hallelujah"


    async def get_todos(self, email: str, session: SessionDep):
        todos = session.exec(select(TodoModel).where(TodoModel.email == email)).all()
        _formated = []
        for todo in todos:
            _formated.append(self._get_in_dict_format(todo=todo))
        return Response(content=json.dumps({"email": email, "todos": _formated}), media_type="json")


    def _get_in_dict_format(self, todo: TodoModel):
        return {
            "email": todo.email,
            "title": todo.title,
            "desc": todo.description,
            "due": todo.due_date,
            "id": todo.id
        }


    async def edit(self, request: Request, id: int, session: SessionDep):
        body = await request.json()
        todo = session.get(TodoModel, id)
        if not todo:
            raise HTTPException(status_code=404, detail="ToDo not found")
        todo.title = body["title"]
        todo.description = body["description"]
        todo.due_date = body["due_date"]
        session.commit()
        session.refresh(todo)
        return todo


    async def get_todo(self, id: int, session: SessionDep):
        todo = session.get(TodoModel, id)
        if not todo:
            raise HTTPException(status_code=404, detail="ToDo not found")
        return todo


    async def delete(self, id: int,  session: SessionDep):
        todo = session.get(TodoModel, id)
        if not todo:
            raise HTTPException(status_code=404, detail="ToDo not found")
        session.delete(todo)
        session.commit()
        return {"ok": True}
