from fastapi import APIRouter
from app.settings import Settings
from app.src.Todos.controller import TodoController

class TodoRouter():
    
    def __init__(self, settings:Settings):
        
        self.settings = settings
        self.router = APIRouter()
        self.controller = TodoController(settings=settings)
        self.router.add_api_route("/todos", self.controller.create, methods=["POST"])
        self.router.add_api_route("/todos/{email}", self.controller.get_todos, methods=["GET"])
        self.router.add_api_route("/todos/{id}", self.controller.edit, methods=["PUT"])
        self.router.add_api_route("/todos/{id}", self.controller.get_todo, methods=["GET"])
        self.router.add_api_route("/todos/{id}", self.controller.delete, methods=["DELETE"])
