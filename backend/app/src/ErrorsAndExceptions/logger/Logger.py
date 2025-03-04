import json
import logging


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CustomLogger(metaclass=SingletonMeta):
    
    def log_error(self, error=None):
        error_data = error
        with open("errors.json") as f:
            json_data = json.load(f)

        json_data["errors"].insert(0, error_data)

        error_data = json_data
        with open('errors.json', "w",) as f:
            json.dump(error_data, f, ensure_ascii=False, indent=4)