import logging
import secrets
from cryptography.fernet import Fernet

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class CSRFProtector(metaclass=SingletonMeta):
    
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]
	
	def __init__(self):
		key = Fernet.generate_key()
		self.fernet = Fernet(key=key)
		self.active_token = None
		self._set_initial_token()


	def _set_initial_token(self):
		secret = secrets.token_hex(24)
		self.token = self.fernet.encrypt(secret.encode())


	def provide_ative_token(self):
		self.active_token = self.fernet.encrypt(self.token).decode()
		return {"token": self.active_token}


	def compare_token(self, token: str):
		try:
			decrypted = self.fernet.decrypt(token=token)
			if decrypted == self.token:
				return True
			return False
		except Exception as e:
			logging.exception(e)
			return False