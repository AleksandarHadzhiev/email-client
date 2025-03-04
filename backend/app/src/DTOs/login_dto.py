from app.src.DTOs.base import BaseDTO


class ExternalServiceLogin(BaseDTO):
    def set_value(self, data: dict):
        super().set_value(data)
        self.email: str=data["email"]


    def get_values_as_dict(self):
        return {
            "email": self.email
        }


class EmailAndPasswordLogin(ExternalServiceLogin):
    def set_value(self, data: dict):
        super().set_value(data)
        self.password: str=data["password"]


    def get_values_as_dict(self):
        return {
            "email": self.email,
            "password": self.password
        }
