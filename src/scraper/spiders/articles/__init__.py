import scrapy
from scrapy.loader import ItemLoader

from scraper.items import ArticleItem
from scraper.processors import parse_date, source_name
from utils import logger


class BBC(scrapy.Spider):
    name = 'bbc_articles'

    def __init__(self, start_urls=None, *args, **kwargs):
        super(BBC, self).__init__(*args, **kwargs)
        if start_urls is not None:
            self.start_urls = start_urls

    def parse(self, response):
        l = ItemLoader(item=ArticleItem(), response=response)
        l.add_value('source_url', response.url)
        l.add_value('source_name', source_name(response.url))
        l.add_xpath('title', '//head/title/text()')
        l.add_value('published_at', parse_date(response))
        l.add_css('body', 'article')
        yield l.load_item()
