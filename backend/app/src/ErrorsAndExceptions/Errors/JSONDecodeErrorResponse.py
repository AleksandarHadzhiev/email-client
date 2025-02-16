import json
from fastapi import Response, status
from app.src.ErrorsAndExceptions.logger.Logger import CustomLogger 
class JSONDecodeErrorResponse():
    
    def __init__(self, msg, endpoint):
        self.message = msg
        self.endpoint = endpoint
        self.logger = CustomLogger()


    def response(self):
        error = {
            "type": "json.decoder.JSONDecodeError",
            "message": self.message,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "endpoint": self.endpoint
        }
        self.logger.log_error(error=error)
        return Response(
                content=json.dumps({
                    "json.decoder.JSONDecodeError:": self.message, 
                    "details": "One or more of the fields in the request body is breaking the JSON format."}), 
                status_code=status.HTTP_400_BAD_REQUEST)