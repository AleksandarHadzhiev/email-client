from app.src.validations.login_validations import BaseEmailValidation,  BaseValidation,  EmailAndPasswordValidation
from app.src.DTOs.login_dto import ExternalServiceLogin, EmailAndPasswordLogin
from app.src.DTOs.EmailDTO import CreateEmailDTO, EmailWithAttachmentsDTO
from app.src.validations.email_object_validation import EmailObjectValidation, EmailWithAttachmentsValidation

class ValidationFactory():
    def __init__(self, incoming_data):
        self.incoming_data = incoming_data
        self.types_of_validation_based_on_incoming_data = {
            ExternalServiceLogin: BaseEmailValidation(),
            EmailAndPasswordLogin: EmailAndPasswordValidation(),
            CreateEmailDTO: EmailObjectValidation(),
            EmailWithAttachmentsDTO: EmailWithAttachmentsValidation(),
        }


    def get_the_needed_type_of_validation(self) -> BaseValidation:
        print(f"INCOMING_DATA: {self.incoming_data}")
        dtos = list(self.types_of_validation_based_on_incoming_data.keys())
        for dto in dtos:
            if type(self.incoming_data) is dto: 
                return self.types_of_validation_based_on_incoming_data[dto]
        # Figure out what to return when fail
        return {
            "fail": "The incoming data is not supported validation system."
        }