from app.src.validations.login_validations import BaseEmailValidation,  BaseValidation,  EmailAndPasswordValidation
from app.src.DTOs.login_dto import ExternalServiceLogin, EmailAndPasswordLogin
from app.src.DTOs.EmailDTO import CreateEmailDTO, EmailWithAttachmentsDTO
from app.src.DTOs.todo_dto import CreateTodoNoDescDTO, CreateTodoDTO, CreateTodoNoDateDTO
from app.src.validations.email_object_validation import EmailObjectValidation, EmailWithAttachmentsValidation
from app.src.validations.todo_object_validation import TodoObjectNoDateValidation, TodoObjectNoDescValidation, TodoObjectValidation

class ValidationFactory():
    def __init__(self, incoming_data):
        self.incoming_data = incoming_data
        self.types_of_validation_based_on_incoming_data = {
            ExternalServiceLogin: BaseEmailValidation(),
            EmailAndPasswordLogin: EmailAndPasswordValidation(),
            CreateEmailDTO: EmailObjectValidation(),
            EmailWithAttachmentsDTO: EmailWithAttachmentsValidation(),
            CreateTodoDTO: TodoObjectValidation(),
            CreateTodoNoDescDTO: TodoObjectNoDescValidation(),
            CreateTodoNoDateDTO: TodoObjectNoDateValidation()
        }


    def get_the_needed_type_of_validation(self) -> BaseValidation:
        dtos = list(self.types_of_validation_based_on_incoming_data.keys())
        for dto in dtos:
            if type(self.incoming_data) is dto: 
                return self.types_of_validation_based_on_incoming_data[dto]
        # Figure out what to return when fail
        return {
            "fail": "The incoming data is not supported validation system."
        }