from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6380
    REDIS_STREAM_NAME: str = "betting_stream"

    SUPERBET_EMAIL: str = ""
    SUPERBET_EMAIL_PASSWORD: str = ""


settings = Settings()
