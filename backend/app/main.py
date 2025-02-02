from app.settings import Settings
from fastapi import FastAPI, Depends
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.src.Login.router import LoginRouter
from app.src.Todos.router import TodoRouter
from app.db import DBConnector
from typing import Annotated
from sqlmodel import Session


settings = Settings()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="session")

db = DBConnector()
SessionDep = Annotated[Session, Depends(db.get_session())]

login_router = LoginRouter(settings=settings)
todo_router = TodoRouter(settings=settings, session=SessionDep)

app.include_router(login_router.router)
app.include_router(todo_router.router)
origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*"
)

@app.get("/")
async def root():
    print("Got Called")
    return '<a class="button" href="/login">Google Login</a>'

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)