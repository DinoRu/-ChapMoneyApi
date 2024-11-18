from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class HashPassword:

	def create_hash(self, password: str):
		return pwd_context.hash(password)

	def verify_hash(self, plain_text: str, hashed_password: str):
		return pwd_context.verify(plain_text, hashed_password)