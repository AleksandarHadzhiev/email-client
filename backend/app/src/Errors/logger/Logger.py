from datetime import datetime
import json

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CustomLogger(metaclass=SingletonMeta):
    
    def log_error(self, error=None):
        
        current_datetime = datetime.now()
        formated_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
        
        error_data = {
            error["type"]: {
                "time": formated_datetime,
                "message": error["message"],
                "status_code": error["status_code"],
                "endpoint": error["endpoint"]
            }
        }

        with open("errors.json") as f:
            json_data = json.load(f)

        json_data["errors"].insert(0, error_data)

        with open('errors.json', "w",) as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)