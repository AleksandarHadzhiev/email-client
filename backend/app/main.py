import json
from app.settings import Settings
from fastapi import FastAPI, Response
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.src.ExternalServices.router import ExternalServiceRouter
from app.src.Todos.router import TodoRouter
from app.db import DBConnector
from app.src.validations.csrf_protector import CSRFProtector

settings = Settings()
db = DBConnector()

csrf_protector = CSRFProtector()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="session")

external_router = ExternalServiceRouter(settings=settings)
todo_router = TodoRouter(settings=settings)

app.include_router(external_router.router)
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


@app.on_event("startup")
def on_startup():
    db.create_db_and_tables()

@app.get("/")
async def root():
    token = csrf_protector.provide_ative_token()
    response = Response(
        content=json.dumps({"message": "Welcome!", "csrf": token["token"]}),
        status_code=200,
    )
    return response
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)