from datetime import datetime
import json
from fastapi import Response
from app.src.ErrorsAndExceptions.logger.Logger import CustomLogger

class ErrorResponse():
    def __init__(self, detail, endpoint, status):
        self.detail = detail
        self.endpoint = endpoint
        self.status = status
        self.logger = CustomLogger()


    def response(self):
        error = {
            "type": "Exception",
            "message": self.detail,
            "status_code": self.status,
            "endpoint": self.endpoint
        }
        self.logger.log_error(error=error)
        return Response(content=json.dumps({"error": self.detail}), status_code=self.status)
    

class Error():
    def __init__(self, detail, endpoint, status):
        self.detail = detail
        self.endpoint = endpoint
        self.status = status
        self.logger = CustomLogger()
        self.type = ""


    def _set_type(self):
        pass


    def as_response(self):
        current_datetime = datetime.now()
        formated_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
        
        error = {
            "type": self.type,
            "message": self.detail,
            "status_code": self.status,
            "endpoint": self.endpoint,
            "time": formated_datetime,
        }
        return error