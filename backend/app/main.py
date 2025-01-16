from app.settings import Settings
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.src.Login.router import LoginRouter


settings = Settings()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="session")

login_router = LoginRouter(settings=settings)
app.include_router(login_router.router)
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