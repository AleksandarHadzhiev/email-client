import json
from app.settings import Settings
from fastapi import FastAPI, Response
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.src.Email.router import EmailRouter
from app.src.Login.router import LoginRouter
from app.src.Todos.router import TodoRouter
from app.db.sqlite import SQLiteConnector
from app.src.validations.csrf_protector import CSRFProtector

 
settings = Settings()
db = SQLiteConnector()

csrf_protector = CSRFProtector()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="session")

todo_router = TodoRouter(settings=settings, db=db)
login_router = LoginRouter(settings=settings)
email_router = EmailRouter(settings=settings)

app.include_router(todo_router.router)
app.include_router(login_router.router)
app.include_router(email_router.router)
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
    uvicorn.run("main:app", host="127.0.0.1", port=5002)