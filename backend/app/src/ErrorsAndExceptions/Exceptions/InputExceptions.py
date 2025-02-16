class NotValidEmailFormatException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class EmailNotInSupportedDomainsException(Exception):
    def __init__(self, *args):
        super().__init__(*args)