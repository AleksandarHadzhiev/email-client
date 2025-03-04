class InputException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class NotValidEmailFormatException(InputException):
    def __init__(self, *args):
        super().__init__(*args)


class EmailNotInSupportedDomainsException(InputException):
    def __init__(self, *args):
        super().__init__(*args)