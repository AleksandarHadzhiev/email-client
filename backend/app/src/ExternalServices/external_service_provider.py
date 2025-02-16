from typing import Protocol
from fastapi import Request

class ExternalServiceProvider(Protocol):
    def __init__(self, settings):
        self.settings = settings


    async def login(self, email: str=None, request:Request=None):
        pass


    async def callback(self, request: Request):
        pass


    async def send_email(self, data):
        pass


    async def get_emails(self):
        pass


    async def get_email_by_id(self, id:str):
        pass