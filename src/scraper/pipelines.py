from abc import ABC, abstractmethod
from typing import Self
from unittest.mock import Base

import scrapy
from google.cloud import bigquery
from itemadapter import ItemAdapter
from pydantic import ValidationError
from scrapy.exceptions import DropItem

from configs.settings import ConfigSettings
from models.web_pages import Article
from services import bq
from services.bq import ArticleService, BqService
from utils import logger


class BasePipeline(ABC):
    @classmethod
    def from_crawler(cls, crawler):
        try:
            pipe = cls.from_settings(crawler.settings)  # type: ignore[attr-defined]
        except AttributeError:
            pipe = cls()
            pipe.crawler = crawler
            pipe._fingerprinter = crawler.request_fingerprinter
        return pipe

    def flush_items(self):
        pass

    def close_spider(self, spider: scrapy.Spider):
        self.flush_items()


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
        self._bq_service: ArticleService = bq.ArticleService()
        self._item_cache = {}

    def close_spider(self, spider: scrapy.Spider):
        super().close_spider(spider)
        self.flush_items()

    def process_item(self, item, spider: scrapy.Spider):
        if 'article' not in self._item_cache:
            self._item_cache = {'article': []}
        self._item_cache['article'].append(item)

        if len(self._item_cache) >= ConfigSettings.bq_cache_limit:
            self.flush_items()
        return item

    def flush_items(self):
        if self.cache_size > 0:
            self._bq_service.save_articles(self._item_cache['article'].copy())
            self._item_cache['article'].clear()

    @property
    def cache_size(self):
        return len(self._item_cache['article'])


class EmbeddingArticlePipeline(BasePipeline):
    def __init__(self):
        self._bq_service: ArticleService = bq.ArticleService()
        self._item_cache = {}

    def process_item(self, item, spider: scrapy.Spider):
        return item
