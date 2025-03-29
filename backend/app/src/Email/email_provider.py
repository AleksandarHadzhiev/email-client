from typing import Protocol
from fastapi import Request

class EmailProvider(Protocol):
    def __init__(self, settings):
        self.settings = settings


    async def send_email(self, data):
        pass


    async def get_emails(self):
        pass


    async def get_email_by_id(self, id):
        pass


    def set_client(self, client):
        self.client = client


    def _get_client(self,):
        return self.client