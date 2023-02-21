import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_NAME: str

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/../.env"


settings = Settings()
