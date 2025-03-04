from app.src.validations.base_validation import BaseValidation

class BaseEmailValidation(BaseValidation):
    
    def __init__(self):
        super().__init__()


    def get_data_if_valid(self, data)-> dict:
        return self._email_validation(email=data["email"])


    def _email_validation(self, email):
        response = self._get_email_if_not_empty_input(email=email)
        if "fail" in response:
            return response
        return self._get_email_if_valid_email_format(email=email)


    def _get_email_if_not_empty_input(self, email: str) -> dict:
        if email.strip() != "":
            return {"email": email}
        return {"fail": f"The provided email: {email} is empty. Please provide email"}


    def _get_email_if_valid_email_format(self, email: str):
        if "@" not in email:
            return {"fail": f"The provided email: {email} is not in valid email. Check for missing '@'."}
        return {"email": email}


class EmailAndPasswordValidation(BaseEmailValidation):

    def __init__(self):
        super().__init__()


    def get_data_if_valid(self, data)-> dict:
        print(f"DATA: {data}")
        response =self._email_validation(email=data["email"])
        if "fail" in response:
            return response
        return self._password_validation(password=data["password"])


    def _password_validation(self, password: str) ->dict:
        if password.strip() != "":
            return {"password": password}
        return {"fail": f"The password email: {password} is empty. Please provide password"}
