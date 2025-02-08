from typing import Optional
from sqlmodel import SQLModel, Field

class TodoModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    title: str = Field(index=True)
    description: str = Field(default=None, index=True)
    status: str = Field(default="In Progress", index=True)
    due_date: str = Field(default=None, index=True)
    