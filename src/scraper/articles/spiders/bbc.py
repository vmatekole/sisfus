import scrapy
from lxml import etree
from rich import print
from scrapy.loader import ItemLoader

from models.web_pages import Article
from scraper.articles.items import ArticleItem
from utils import logger

# from models.web_pages import Author


class BBC(scrapy.Spider):
    name = 'bbc_articles'

    def __init__(self, start_urls=None, *args, **kwargs):
        super(BBC, self).__init__(*args, **kwargs)
        if start_urls is not None:
            self.start_urls = start_urls

    def parse(self, response):
        l = ItemLoader(item=ArticleItem(), response=response)
        l.add_css('title', 'article h1:first-of-type::text')
        l.add_css('created_at', 'article time::text')
        l.add_css('body', 'article')
        yield l.load_item()
