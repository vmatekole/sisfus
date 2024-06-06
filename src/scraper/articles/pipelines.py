from unittest.mock import Base

from google.cloud import bigquery
from itemadapter import ItemAdapter
from pydantic import ValidationError
from scrapy.exceptions import DropItem

from configs.settings import ConfigSettings
from models.web_pages import Article
from services import bq
from services.bq import ArticleService, BqService
from utils import logger


class BasePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        try:
            pipe = cls.from_settings(crawler.settings)  # type: ignore[attr-defined]
        except AttributeError:
            pipe = cls()
        pipe.crawler = crawler
        pipe._fingerprinter = crawler.request_fingerprinter
        return pipe


class ArticleValidationPipeline(BasePipeline):
    def process_item(self, item, spider):
        try:
            valid_article = Article(**item)
            return valid_article
        except ValidationError as e:
            spider.logger.error(f'Invalid item {e}')
            raise DropItem(f'Item validation failed: {e}')


class BigQueryArticlePipeline(BasePipeline):
    def __init__(self):
        self._bq_service: ArticleService = bq.ArticleService(bigquery.Client())
        self._item_cache = {}

    def process_item(self, item, spider):
        c = None
        if ConfigSettings.bq_articles_table_id not in self._item_cache:
            self._item_cache[ConfigSettings.bq_articles_table_id] = []
            c = self._item_cache[ConfigSettings.bq_articles_table_id]

        c.append(item)
        self.flush_items()
        return item

    def flush_items(self):
        c = self._item_cache[ConfigSettings.bq_articles_table_id]
        if len(c) >= ConfigSettings.bq_cache_limit:
            self._bq_service.save_articles(c)
