import json

from fastapi import APIRouter, Request
from app.settings import Settings
from app.src.Todos.service import ToDoService

class TodoRouter():
    
    def __init__(self, settings:Settings):
        self.settings = settings
        self.router = APIRouter()
        self.service = ToDoService(settings=settings)
        self.router.add_api_route("/", self.create, methods=["POST"])
        self.router.add_api_route("/{user_id}", self.get_todos, methods=["GET"])
        self.router.add_api_route("/{todo_id}", self.edit, methods=["PUT"])
        self.router.add_api_route("/{todo_id}", self.delete, methods=["DELETE"])
        

    async def create(self, request: Request):
        print(await request)
        pass


    async def get_todos(self, user_id: int):
        pass


    async def edit(self, request: Request, todo_id: int):
        print(await request)
        pass


    async def delete(self, todo_id: int):
        pass
