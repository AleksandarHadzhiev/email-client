from datetime import datetime
from app.src.validations.Fields.base import BaseFieldType
from app.src.validations.email_validation import BaseEmailValidation

class EmailField(BaseFieldType):
    def __init__(self):
        super().__init__()
        self.email_validation = BaseEmailValidation()


    def validate(self, data):
        validatiaon_response = self.email_validation.get_data_if_valid(data=data)
        if "fail" in validatiaon_response:
            return validatiaon_response
        return data


class DateField(BaseFieldType):
    def __init__(self):
        super().__init__()


    def validate(self, data):
        if str(data).strip() == "":
            return
        try:
            if data == datetime.strptime(data,  "%d/%m/%Y, %H:%M:%S").strftime( "%d/%m/%Y, %H:%M:%S"):
                return data
        except ValueError:
            return {"fail": "The date format is not the one supported by the service. The correct format is: %d/%m/%Y, %H:%M:%S"}


class SubjectField(BaseFieldType):
    def __init__(self):
        super().__init__()


    def validate(self, data):
        super().validate(data)
        if str(data).strip() == "":
            return {"fail": "Subject field is mandatory."}
        return data


class BodyField(BaseFieldType):
    def __init__(self):
        super().__init__()


    def validate(self, data):
        super().validate(data)
        if str(data).strip() == "":
            return {"fail": "Body field is mandatory."}
        return data


class AttachmentsField(BaseFieldType):
    def __init__(self):
        super().__init__()


    def validate(self, data):
        if list(data).__len__() == 0:
            return {"fail": "Sending an attachments email, without attachments."}
        # TO DO: 
        # Adding more checks for an attachment itself.
        return data
        