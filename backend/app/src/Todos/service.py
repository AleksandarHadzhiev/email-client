class ToDoService():
    
    def __init__(self, settings):
        self.settings = settings


    def validate_incoming_data(self, todo):
        pass


    def _validate_empty_input(self, todo):
        for element in todo:
            if element == "":
                return "empty"
        return ""


    def _validate_email_format(self, email):    
        if "@" not in email:
            return "incorrect format"
