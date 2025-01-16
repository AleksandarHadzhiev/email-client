import unittest
from app.src.Factory.LoginFactory import LoginFactory
from app.src.Errors.LoginFactoryErrors import NotSupportedDomain, NotValidEmail


class TestLoginFactory(unittest.TestCase):
    
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)


    def test_not_valid_email_format(self):
        invalid_format_email = "aleks"
        with self.assertRaises(NotValidEmail) as exception:
            self.login_factory = LoginFactory(email=invalid_format_email)
        self.assertEqual(str(exception.exception), f"The email is invalid")


    def test_not_supported_domain_ends_on_nl(self):
        not_supported_domain = "aleks@gmail.nl"
        with self.assertRaises(NotSupportedDomain) as exception:
            self.login_factory = LoginFactory(email=not_supported_domain)
        self.assertEqual(str(exception.exception), f"The email is not from supported domain")

    def test_not_supported_domain_ends_on_not_google_or_outlook(self):
        not_supported_domain = "aleks@bgmail.com"
        with self.assertRaises(NotSupportedDomain) as exception:
            self.login_factory = LoginFactory(email=not_supported_domain)
        self.assertEqual(str(exception.exception), f"The email is not from supported domain")


if __name__ == "__main__":
    unittest.main()
