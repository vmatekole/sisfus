from itemadapter import ItemAdapter
from pydantic import ValidationError
from scrapy.exceptions import DropItem

from models.web_pages import Article
from utils import logger


class ArticlePipeline:
    def process_item(self, item, spider):
        # Validate item
        # Persist to bigquery
        try:
            valid_article = Article(**item)
            return valid_article.model_dump()
        except ValidationError as e:
            spider.logger.error(f'Invalid item {e}')
            raise DropItem(f'Item validation failed: {e}')

    @classmethod
    def from_crawler(cls, crawler):
        try:
            pipe = cls.from_settings(crawler.settings)  # type: ignore[attr-defined]
        except AttributeError:
            pipe = cls()
        pipe.crawler = crawler
        pipe._fingerprinter = crawler.request_fingerprinter
        return pipe
