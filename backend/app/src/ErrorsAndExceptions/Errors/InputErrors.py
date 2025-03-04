import json
from fastapi import Response, status
from app.src.ErrorsAndExceptions.Errors.TodoErrors import Error


class InputError(Error):
    def __init__(self, input: str, error_message: str, status: status, endpoint: dict):
        self.input = input,
        super().__init__(detail=error_message, endpoint=endpoint, status=status)
        self.error_message=error_message
        self._set_type()


    def _set_type(self):
        self.type = "InputError"


    def as_response(self):
        error = super().as_response()
        error["input"] = self.input
        self.logger.log_error(error=error)
        return Response(content=json.dumps({"error": self.error_message}), status_code=self.status)


class InvalidEmail(InputError):
    def __init__(self, input_type: str, error_message: str, status: status, endpoint: dict):
        super().__init__(input_type=input_type, error_message=error_message, status=status, endpoint=endpoint)


    def _set_type(self):
        self.type = "InvalidEmail"


    def as_response(self):
        return super().as_response()


class UnsupportedDomainError(InputError):
    def __init__(self, input_type: str, error_message: str, status: status, endpoint: dict):
        super().__init__(input_type=input_type, error_message=error_message, status=status, endpoint=endpoint)


    def _set_type(self):
        self.type = "UnsupportedDomainError"


    def as_response(self):
        return super().as_response()
