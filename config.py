"""
Модуль конфига бота.
"""
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    BOT_TOKEN: str
    SERV_URL: str


base_config = Config(_env_file='.env')
