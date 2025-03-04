from app.src.validations.Fields.email_fields import EmailField, DateField, SubjectField, BodyField
from app.src.DTOs.base import BaseDTO


class CreateEmailDTO(BaseDTO):
    def __init__(self):
        super().__init__()


    def set_value(self, data):
        super().set_value(data)
        self.to: EmailField = data["to"]
        self._from: EmailField = data["from"]
        self.date: DateField = data["date"]
        self.subject: SubjectField = data["subject"]
        self.body: BodyField = data["body"]
        

    def get_values_as_dict(self) -> dict:
        return {
            "to": self.to,
            "from": self._from,
            "date": self.date,
            "subject": self.subject,
            "body": self.body,
        }


class EmailWithAttachmentsDTO(CreateEmailDTO):
    def set_value(self, data):
        super().set_value(data)
        self.attachments: BodyField = data["attachments"]


    def get_values_as_dict(self):
        base_email = super().get_values_as_dict()
        base_email["attachments"] = self.attachments
        return base_email