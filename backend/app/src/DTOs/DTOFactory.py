from app.src.DTOs.login_dto import ExternalServiceLogin, EmailAndPasswordLogin, BaseDTO
from app.src.DTOs.EmailDTO import CreateEmailDTO, EmailWithAttachmentsDTO
from app.src.DTOs.todo_dto import CreateTodoDTO, CreateTodoNoDescDTO, CreateTodoNoDateDTO


class DTOFactory:
    def __init__(self, data: dict):
        self.data = data
        self.supported_dtos = [
            [{"email":""},ExternalServiceLogin()],
            [{"email":"", "password": ""},EmailAndPasswordLogin()],
            [{"email":"", "password": "", "username": ""},EmailAndPasswordLogin()],
            [{"to": "", "from": "", "date": "", "subject": "", "body": ""}, CreateEmailDTO()],
            [{"to": "", "from": "", "date": "", "subject": "", "body": "", "attachments": []}, EmailWithAttachmentsDTO()],
            [{"title": "", "description": "", "due_date": "", "email": ""}, CreateTodoDTO()],
            [{"title": "", "due_date": "",  "email": ""}, CreateTodoNoDescDTO()],
            [{"title": "", "email": ""}, CreateTodoNoDateDTO()],
        ]


    def get_dto_based_on_incoming_data(self):
        for dto in self.supported_dtos:
            
            dto_keys = list(dict(dto[0]).keys())
            incoming_data_keys = list(self.data.keys())
            if incoming_data_keys == dto_keys:
                _dto: BaseDTO = dto[1]
                _dto.set_value(data=self.data)
                return _dto
        # Something to return if the data format is not supported/
        return {
            "fail": "The incomind data is not supported format."
        }