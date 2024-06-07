from client.bq import Bq
from configs.settings import ConfigSettings, Settings
from utils import logger

config: Settings = ConfigSettings


class BqService:
    def __init__(self, client) -> None:
        self._client = client
        self._bq = Bq(client)


class ArticleService(BqService):
    def __init__(self, client) -> None:
        super().__init__(client)

    def save_articles(self, articles):

        return self._bq.insert_to_bigquery(
            articles,
            'article',
        )

    def save_text_embeddings(self, embeddings):

        return self._bq.insert_to_bigquery(
            embeddings,
            'text_embeddings',
        )
