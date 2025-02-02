import json

from fastapi import APIRouter, Request, Response
from app.settings import Settings
from app.src.Todos.service import ToDoService
from sqlmodel import Session
class TodoRouter():
    
    def __init__(self, settings:Settings, session: Session):
        self.settings = settings
        self.session = session
        self.router = APIRouter()
        self.service = ToDoService(settings=settings)
        self.router.add_api_route("/todo", self.index, methods=["GET"])
        self.router.add_api_route("/todo", self.create, methods=["POST"])
        self.router.add_api_route("/todo/{email}", self.get_todos, methods=["GET"])
        self.router.add_api_route("/todo/{id}", self.edit, methods=["PUT"])
        self.router.add_api_route("/todo/{id}", self.delete, methods=["DELETE"])


    async def index(self):
        return  '<a class="button" href="/login">ToDo Login</a>'


    async def create(self, request: Request):
        print(await request)
        pass


    async def get_todos(self, email: str):
        return Response(content=json.dumps({"email": email}), media_type="json")


    async def edit(self, request: Request, id: int):
        print(await request)
        pass


    async def delete(self, id: int):
        pass
