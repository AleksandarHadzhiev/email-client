from pydantic import BaseModel

class ToDo(BaseModel):
    email: str
    title: str
    description: str
    due_date: str