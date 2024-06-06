from client.bq import Bq
from configs.settings import ConfigSettings, Settings
from utils import logger


class BqService:
    def __init__(self, client) -> None:
        self._client = client
        self._bq = Bq(client)


class ArticleService(BqService):
    def __init__(self, client) -> None:
        super().__init__(client)

    def save_articles(self, articles):

        config: Settings = ConfigSettings
        return self._bq.insert_to_bigquery(
            articles,
            config.gcp_project_id,
            config.bq_dataset_id,
            config.bq_articles_table_id,
        )
