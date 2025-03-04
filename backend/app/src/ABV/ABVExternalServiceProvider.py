from datetime import datetime, timedelta, timezone
import secrets

import jwt
from app.src.ExternalServices.external_service_provider import ExternalServiceProvider
from urllib.parse import parse_qs, urlparse
import poplib, email
from cryptography.fernet import Fernet
from app.src.modules.email import Email

# user = "df_er@abv.bg"
# passwrod = "12132123aah"

# Mailbox = poplib.POP3_SSL(host="pop3.abv.bg", port=995)
# Mailbox.user(user=user)
# Mailbox.pass_(pswd=passwrod)
# NumOfMessages = len(Mailbox.list()[1])
# for i in range(NumOfMessages):
#     for msg in Mailbox.retr(i+1)[1]:
#         print(msg)
# Mailbox.quit()
# print(NumOfMessages)

class ABV(ExternalServiceProvider):
    def __init__(self, settings):
        super().__init__(settings)
        self.algorithm = 'HS256'
        self.jwt_secret = secrets.token_hex(24)
        self.fernet = self._generate_security_block()


    def _generate_security_block(self)->Fernet:
        key = Fernet.generate_key()
        return Fernet(key=key)


    async def login(self, data: dict = None, request = None) -> dict:
        await super().login(data, request)
        # Login to IMAP Server, so you can fetch emails.
        Mailbox = poplib.POP3_SSL(host="pop3.abv.bg", port=995)
        try:
            Mailbox.user(user=data["email"])
            Mailbox.pass_(pswd=data["password"])
            self._set_mailbox(mailbox=Mailbox)
            return self._encrypt_outgoing_data(data=data)
        except poplib.error_proto as e:
            return {"fail": str(e), "reason": "The credentials provided do not exist in the email provider abv.bg"}


    def _set_mailbox(self, mailbox:poplib.POP3_SSL):
        self.mailbox = mailbox


    def _encrypt_outgoing_data(self, data:dict)->dict:
        encrypted_email =self.fernet.encrypt(str(data["email"]).encode())
        encrypted_password = self.fernet.encrypt(str(data["password"]).encode())
        return {"redirect_uri": f"{self.settings.FRONTEND_URL}/auth?name={encrypted_email.decode()}&prot={encrypted_password.decode()}&external=1"}


    async def callback(self, request):
        email = await self._decrypt_data(request=request)
        return self._generate_jwt(email=email)


    async def _decrypt_data(self, request):
        body = await request.json()
        pathname = body["pathname"]
        parse_res = urlparse(pathname)
        query_params = parse_qs(parse_res.query)
        print("PARAMS")
        print(query_params)
        email = query_params["name"][0]
        return email


    def _generate_jwt(self, email):
        decrypted_email = self.fernet.decrypt(email).decode()
        print(decrypted_email)
        payload = {
            "email": decrypted_email,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=3)
        }

        token = jwt.encode(payload=payload, key=self.jwt_secret, algorithm='HS256')
        encrypted_token = self.fernet.encrypt(token.encode())
        return {"token": encrypted_token.decode(), "email": decrypted_email}


    async def get_emails(self):
        NumOfMessages = len(self.mailbox.list()[1])
        messages = []
        for i in range(NumOfMessages):
            print(f"I: {i}")
            emails = self.mailbox.retr(i+1)[1]
            messages = Email("", email_service="").get_email_content_for_pop3(emails=emails, messages=messages)
        return messages
