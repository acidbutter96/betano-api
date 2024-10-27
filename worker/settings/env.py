from dotenv import load_dotenv
from dotenv import dotenv_values
from functools import cached_property


class EnvironmentVariables:
    def __init__(self, dotenv_path: str = "./.env",):
        load_dotenv(dotenv_path=dotenv_path, override=True,)
        self.values = dotenv_values(dotenv_path)
        for key, value in self.values.items():
            print(key, value)
            setattr(self, key, value)

    @cached_property
    def redis_url(self,):
        if getattr(self, 'REDIS_URL', False) or getattr(self, 'REDIS_PORT', False):
            return f"redis://{self.REDIS_URL}:{self.REDIS_PORT}"
        return "redis://localhost:6666"


env = EnvironmentVariables()
