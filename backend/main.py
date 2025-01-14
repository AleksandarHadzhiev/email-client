from settings import Settings
from fastapi import FastAPI
import uvicorn
from src.Google.router import GoogleRouter
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()
app = FastAPI()
google_router = GoogleRouter(settings)
app.include_router(google_router.router)
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