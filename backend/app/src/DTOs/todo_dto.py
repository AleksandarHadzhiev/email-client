from app.src.DTOs.base import BaseDTO


class CreateTodoNoDateDTO(BaseDTO):
    def set_value(self, data):
        self.title: str = data["title"]
        self.email: str = data["email"]


    def get_values_as_dict(self):
        return {
            "title": self.title,
            "email": self.email
        }


class CreateTodoNoDescDTO(CreateTodoNoDateDTO):
    def set_value(self, data):
        super().set_value(data=data)
        self.date: str = data["due_date"]


    def get_values_as_dict(self):
        data = super().get_values_as_dict()
        data["date"] = self.date
        return data


class CreateTodoDTO(CreateTodoNoDescDTO):
    def set_value(self, data):
        super().set_value(data=data)
        self.description: str = data["description"]


    def get_values_as_dict(self):
        data = super().get_values_as_dict()
        data["description"] = self.description
        return data