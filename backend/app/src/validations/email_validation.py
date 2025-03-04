from app.src.validations.base_validation import BaseValidation

class BaseEmailValidation(BaseValidation):
    
    def __init__(self):
        super().__init__()


    def get_data_if_valid(self, data)-> dict:
        response = self._get_email_if_not_empty_input(email=data)
        if "fail" in response:
            return response
        return self._get_email_if_valid_email_format(email=data)


    def _get_email_if_not_empty_input(self, email: str) -> dict:
        if email.strip() != "":
            return {"email": email}
        return {"fail": f"The provided email: {email} is empty. Please provide email"}


    def _get_email_if_valid_email_format(self, email: str):
        if "@" not in email:
            return {"fail": f"The provided email: {email} is not in valid email. Check for missing '@'."}
        return {"email": email}