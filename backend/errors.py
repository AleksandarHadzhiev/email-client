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
		print(f"ACTIVE: {self.active_token}")
		return {"token": self.active_token}


	def compare_token(self, token: str):
		print(token)
		try:
			decrypted = self.fernet.decrypt(token=token)
			print(f"DECRYPTED: {decrypted}")
			if decrypted == self.token:
				return True
			return False
		except Exception as e:
			print(e)
			return False


# csrf_protecotor = CSRFProtector()
# Old_token = csrf_protecotor.provide_ative_token()

# result = csrf_protecotor.compare_token(token=Old_token["token"])
# print(f"AUTHORIED expected :{result}")

# new_token = csrf_protecotor.provide_ative_token()
# result = csrf_protecotor.compare_token(token=Old_token["token"])
# print(f"UNAUTHORIED expected :{result}")

# result = csrf_protecotor.compare_token(token=new_token["token"])
# print(f"AUTHORIED expected :{result}")


# csrf_protecotor = CSRFProtector()
# result = csrf_protecotor.compare_token(token=new_token["token"])
# print(f"AUTHORIED expected :{result}")

# key = Fernet.generate_key()
# fernet = Fernet(key=key)


# secret = secrets.token_hex(24)
# print(secret)
# algorithm = 'HS256'
# email = "aleks@abv.bg"
# encrypted_email = fernet.encrypt(email.encode())
# payload = {
# 	"email": encrypted_email.decode(),
# 	"exp": datetime.now(timezone.utc) + timedelta(seconds=3)
# }


# token = jwt.encode(payload=payload, key=secret, algorithm=algorithm)
# allowed_token = token
# print(token)

# decoded_data = jwt.decode(token, key=secret, algorithms=algorithm)
# print(decoded_data)
# email_from_token = decoded_data["email"]
# print(type(email_from_token),email_from_token)

# decrypted_email = fernet.decrypt(email_from_token).decode()
# print(decrypted_email)
# time.sleep(3)
# try:
#     decoded_data = jwt.decode(token, key=secret, algorithms=algorithm)
#     print(decoded_data)
# except jwt.ExpiredSignatureError as e:
# 	logging.error(e)

