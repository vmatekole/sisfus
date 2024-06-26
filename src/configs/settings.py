import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding='utf-8')
    log_level: str
    bq_dataset_id: str
    gcp_project_id: str
    bq_dataset_id: str
    item_cache_limit: int
    openai_key: str
    test_without_bigquery: bool
    article_embed_model: str


ConfigSettings = Settings(_env_file=os.environ['SETTINGS_ENV_FILE'])
