import json
from fastapi import Response
from app.src.Errors.logger.Logger import CustomLogger

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