from app.src.validations.base_validation import BaseValidation
from app.src.validations.Fields.email_fields import *

class EmailObjectValidation(BaseValidation):    
    def __init__(self):
        super().__init__()
        self.required_fields = {
            "to": EmailField(),
            "from": EmailField(),
            "date": DateField(),
            "subject": SubjectField(),
            "body": BodyField(), 
        }


    def get_data_if_valid(self, data)-> dict:
        validation_of_keys = self._check_for_missing_required_fields(body=data)
        if "fail" in validation_of_keys:
            return validation_of_keys
        return self._check_if_valid_values(body=data)


    def _check_for_missing_required_fields(self, body: dict) -> dict:
        expected_keys = list(self.required_fields.keys())
        incoming_keys = list(body.keys())
        missing_keys = []
        for key in expected_keys:
            if key not in incoming_keys:
                missing_keys.append(key)
        if missing_keys.__len__() == 0:
            return body
        return {"fail": {"error": "Missing keys in incoming data", "missing_keys": missing_keys}}


    def _check_if_valid_values(self, body:dict) -> dict:
        incoming_keys = list(body.keys())
        for key in incoming_keys:
            element: BaseFieldType = self.required_fields[key]
            validated_values = element.validate(data=body[key])
            if "fail" in validated_values:
                return validated_values
        return body


class EmailWithAttachmentsValidation(EmailObjectValidation):
    def __init__(self):
        super().__init__()
        self.required_fields["attachments"] = AttachmentsField()