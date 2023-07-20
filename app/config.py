from pydantic import BaseSettings


class Base(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'
        env_encoding = 'utf-8'


settings = Base()
