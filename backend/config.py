from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    owner_email: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    google_client_id: str
    google_client_secret: str
    ms_api_key: str
    ms_domain: str

    class Config:
        env_file = "../.env"


settings = Settings()
