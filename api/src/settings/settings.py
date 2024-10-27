from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_QUEUE_NAME: str = "task_queue"

    SUPERBET_EMAIL: str = ""
    SUPERBET_EMAIL_PASSWORD: str = ""


env = Settings()
