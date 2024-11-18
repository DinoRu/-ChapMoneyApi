from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv(dotenv_path="../.env")

class Settings(BaseSettings):
	env: str = 'local'
	app_env: str
	app_debug: str
	database_url: str
	async_database_uri: str
	postgres_db: str
	postgres_host: str
	postgres_user: str
	postgres_password: str
	test_database_url: str
	secret_key: str
	algorithm: str
	token_expires_hours: int
	mail_username: str
	mail_password: str
	mail_port: str
	mail_server: str
	mail_starttls: bool
	mail_ssl_tls: bool
	mail_from: str
	mail_from_name: str
	mail_validate_cert: bool
	authjwt_secret_key: str
	auth_header_type: str
	authjwt_header_name: str
	access_token_expires: int
	refresh_token_expires: int

	def active_database_url(self):
		return self.async_database_uri if self.env == 'docker' else self.database_url

	class Config:
		env_file= "../.env"

