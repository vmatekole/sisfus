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
from tasks.embedding_tasks import embed_batch
from utils import logger


class BasePipeline(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._item_cache = {}

    @classmethod
    def from_crawler(cls, crawler):
        try:
            pipe = cls.from_settings(crawler.settings)  # type: ignore[attr-defined]
        except AttributeError:
            pipe = cls()
            pipe.crawler = crawler
            pipe._fingerprinter = crawler.request_fingerprinter
        return pipe

    def process_item(self, item, spider):
        pass

    def close_spider(self, spider: scrapy.Spider):
        self.flush_items()

    @property
    def cache_size(self):
        return 0


class ArticleValidationPipeline(BasePipeline):
    def __init__(self):
        super().__init__()

    def process_item(self, item, spider):
        try:
            valid_article = Article(**item)
            return valid_article
        except ValidationError as e:
            spider.logger.error(f'Invalid item {e}')
            raise DropItem(f'Item validation failed: {e}')


class BigQueryArticlePipeline(BasePipeline):
    def __init__(self):
        super().__init__()
        self._bq_service: ArticleService = bq.ArticleService()

    def close_spider(self, spider: scrapy.Spider):
        super().close_spider(spider)
        self.flush_items()

    @property
    def cache_size(self):
        return len(self._item_cache['article']) if 'article' in self._item_cache else 0

    def process_item(self, a: Article, spider):
        if 'article' not in self._item_cache:
            self._item_cache = {'article': []}
        self._item_cache['article'].append(a)

        if self.cache_size >= ConfigSettings.item_cache_limit:
            self.flush_items()
        return a

    def flush_items(self):
        if self.cache_size > 0:
            self._bq_service.save_articles(self._item_cache['article'].copy())
            self._item_cache['article'].clear()


class EmbeddingArticlePipeline(BasePipeline):
    def __init__(self):
        self._bq_service: ArticleService = bq.ArticleService()
        self.model_name = ConfigSettings.article_embed_model

    @property
    def cache_size(self):
        return len(self._item_cache['article']) if 'article' in self._item_cache else 0

    async def process_item(self, a: Article, spider):
        if 'article' not in self._item_cache:
            self._item_cache = {'article': []}
        self._item_cache['article'].append(a)

        if self.cache_size >= ConfigSettings.item_cache_limit:
            embeddings: list[float] = await embed_batch(
                self.model_name, self._item_cache['article'].copy()
            )
            for i, e in enumerate(embeddings):
                self._item_cache['article'][i].emedding = e
        return a

    async def flush_items(self):
        if self.cache_size > 0:
            embeddings: list[float] = await embed_batch(
                self.model_name, self._item_cache['article'].copy()
            )
            for i, e in enumerate(embeddings):
                self._item_cache['article'][i].emedding = e
