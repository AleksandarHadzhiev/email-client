from app.src.Factory.LoginFactory import LoginFactory

class LoginService():
    
    def __init__(self, settings):
        self.settings = settings


    def set_login_factory(self, email):
        self.login_factory = LoginFactory(email=email)


    def get_sso(self):
        return self.login_factory.get_sso_based_on_domain(settings=self.settings)