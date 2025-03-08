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
            return {"fail": "Date field is mandatory."}
        try:
            if data == datetime.strptime(data,  "%Y-%m-%d").strftime("%Y-%m-%d"):
                return data
        except ValueError:
            return {"fail": "The date format is not the one supported by the service. The correct format is: %Y-%m-%d"}


class TitleField(BaseFieldType):
    def __init__(self):
        super().__init__()


    def validate(self, data):
        super().validate(data)
        if str(data).strip() == "":
            return {"fail": "TItle field is mandatory."}
        return data



class DescriptionField(BaseFieldType):
    def __init__(self):
        super().__init__()


    def validate(self, data):
        super().validate(data)
        if str(data).strip() == "":
            return {"fail": "Description field is mandatory."}
        return data