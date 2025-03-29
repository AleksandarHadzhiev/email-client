from typing import Protocol
from fastapi import Request

class SSOProvider(Protocol):
    def __init__(self, settings):
        self.settings = settings


    async def login(self, data: dict, request:Request=None):
        pass


    async def auth(self, request: Request):
        pass

