from fastapi import status
from app.src.Errors.TodoErrors import Error


class InputError(Error):
    def __init__(self, input_type: str, error_message: str, status: status, endpoint: dict):
        self.input_type = input_type,
        super().__init__(detail=error_message, endpoint=endpoint, status=status)
        self._set_type()


    def _set_type(self):
        self.type = "InputError"


    def get_error(self):
        return super().get_error()


class InvalidEmail(InputError):
    def __init__(self, input_type: str, error_message: str, status: status, endpoint: dict):
        super().__init__(input_type=input_type, error_message=error_message, status=status, endpoint=endpoint)


    def _set_type(self):
        self.type = "InvalidEmail"


    def get_error(self):
        return super().get_error()


class UnsupportedDomainError(InputError):
    def __init__(self, input_type: str, error_message: str, status: status, endpoint: dict):
        super().__init__(input_type=input_type, error_message=error_message, status=status, endpoint=endpoint)

    def _set_type(self):
        self.type = "UnsupportedDomainError"


    def get_error(self):
        return super().get_error()
