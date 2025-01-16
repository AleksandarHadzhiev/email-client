class NotValidEmail(Exception):

    def __init__(self):
        super().__init__(self._generate_message_for_email())


    def _generate_message_for_email(self):
        return "The email is invalid"


class NotSupportedDomain(Exception):

    def __init__(self):
        super().__init__(self._generate_message_for_email())


    def _generate_message_for_email(self):
        return f"The email is not from supported domain"
