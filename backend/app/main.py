from app.settings import Settings
from fastapi import FastAPI
import uvicorn
from src.Google.router import GoogleRouter
from src.Microsoft.router import MicrosoftRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

settings = Settings()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="session")

google_router = GoogleRouter(settings)
microsoft_router = MicrosoftRouter(settings)
app.include_router(google_router.router)
app.include_router(microsoft_router.router)
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