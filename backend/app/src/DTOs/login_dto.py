from app.src.DTOs.base import BaseDTO


class ExternalServiceLogin(BaseDTO):
    def set_value(self, data: dict):
        super().set_value(data)
        self._assign_email_value(data)


    def _assign_email_value(self, data):
        if 'email' in data:
            self.email = data["email"]
        else:
            self.email = ""

    def get_values_as_dict(self):
        return {
            "email": self.email
        }


class EmailAndPasswordLogin(ExternalServiceLogin):
    def set_value(self, data: dict):
        super().set_value(data)
        self._assign_pass_value(data)


    def _assign_pass_value(self, data):
        if 'password' in data:
            self.password = data["password"]
        else:
            self.password = ""

    def get_values_as_dict(self):
        return {
            "email": self.email,
            "password": self.password
        }
