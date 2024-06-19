from typing import Any

import scrapy
from scrapy.loader import ItemLoader

from scraper.items import ArticleItem
from scraper.processors import parse_date, source_name
from utils import logger


class BaseSpider(scrapy.Spider):
    def __init__(self, name: str | None = None, **kwargs: Any):
        self._failed_items = []
        super().__init__(name, **kwargs)

    @property
    def failed_items(self):
        return self._failed_items


class BBC(BaseSpider):
    name = 'bbc_articles'

    def __init__(self, start_urls=None, *args, **kwargs):
        super(BBC, self).__init__(*args, **kwargs)
        if start_urls is not None:
            self.start_urls = start_urls
        self._failed_items = []

    def parse(self, response):
        # try:
        l = ItemLoader(item=ArticleItem(), response=response)
        l.add_value('source_url', response.url)
        l.add_value('source_name', source_name(response.url))
        l.add_xpath('title', '//head/title/text()')
        l.add_value('published_at', parse_date(response))
        l.add_css('body', 'article')
        yield l.load_item()
        # except Exception as e:
        #     failed_item =  {
        #         'url': response.url,
        #         'error': str(e),
        #         'status': 'failed'
        #     }
        #     self._failed_items.append(failed_item)
        #     raise failed_item
