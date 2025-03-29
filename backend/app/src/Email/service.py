import poplib
from app.settings import Settings
from app.src.Email.provider_factory import EmailProviderFactory
from app.src.Login.SSO.SSO_provider import SSOProvider
from app.src.DTOs.login_dto import BaseDTO
from app.src.validations.base_validation import BaseValidation
from app.src.validations.validation_factory import ValidationFactory
from app.src.Email.Provider.Google import Google
from fastapi import Request


class EmailService():
    def __init__(self, settings: Settings):
        self.settings = settings


    def set_provider(self, provider):
        self.provoder = provider


    # def set_provider(self, client):
    #     self.client = client
    #     provider_factory = EmailProviderFactory(sso_provider=client, settings=self.settings)
    #     response = provider_factory.get_email_provider()
    #     print(response)
    #     if "provider" in response:
    #         self.provoder = response["provider"]
    #     self.provoder = None
        
        

    def _get_provider(self) -> SSOProvider:
        return self.provoder


    def _set_mailbox(self, mailbox: poplib.POP3_SSL):
        self.mailbox = mailbox


    def _get_mailbox(self) -> poplib.POP3_SSL:
        return self.mailbox
 

    def get_mails(self, request: Request, creds: dict):
        print("IN GET MAILS")
        print(creds)
        provider = Google(settings=self.settings)
        provider.set_data_for_mail_creds(creds)
        self.provider = provider
        if provider:
            mails = provider.get_emails()
            return mails
        return None


    async def send_email(self, body: BaseDTO):
        factory = ValidationFactory(incoming_data=body)
        email_object_validation = factory.get_the_needed_type_of_validation()
        if issubclass(type(email_object_validation), BaseValidation) == False:
            return email_object_validation
        response = email_object_validation.get_data_if_valid(data=body.get_values_as_dict())
        if "fail" in response:
            return response
        response = await self.provider.send_email(data=body.get_values_as_dict())
        return response


    async def get_mail_by_id(self, id:str):
        email = self.provider.get_email_by_id(id=id)
        return email
