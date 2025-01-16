from app.src.Errors.LoginFactoryErrors import NotValidEmail, NotSupportedDomain

class LoginFactory():
    
    def __init__(self, email):
        self.email = self.set_email(email=email)
        self.supported_domains = ["@gmail.com", "@outlook.com"]
        self.domain = self.set_domain()


    def set_email(self, email):
        if "@" not in email:
            raise NotValidEmail
        return email


    def set_domain(self):
        # Set the domain of the email
        domain = self._check_domain()

        if domain == "invalid":
            raise NotSupportedDomain
        return domain


    def _check_domain(self):
        for supported_domain in self.supported_domains:
            is_in_domains = str(self.email).endswith(supported_domain)
            if is_in_domains and supported_domain == "gmail.com":
                return "google"
            elif is_in_domains and supported_domain == "outlook.com":
                return "microsoft"
        return "invalid"


    def get_sso_based_on_domain(self):
        if self.domain == "google":
            return "Google email"
        elif self.domain == "microsoft":
            return "Microsoft email"
        return
