import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding='utf-8')


ConfigSettings = Settings(_env_file=os.environ['SETTINGS_ENV_FILE'])
