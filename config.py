"""
Модуль конфига бота.
"""
from pydantic_settings import BaseSettings



class Config(BaseSettings):
    BOT_TOKEN: str

    FACULTIES_URL: str
    EQUIPMENTS_URL: str
    FREE_PLACES_URL: str
    LESSONS_NUM_URL: str

    SERV_URL: str

base_config = Config(_env_file='.env')