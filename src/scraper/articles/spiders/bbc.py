import scrapy
from lxml import etree
from rich import print
from scrapy.loader import ItemLoader

from base.utils import logger
from models.web_pages import Article
from scraper.articles.items import ArticleItem

# from models.web_pages import Author


class BBC(scrapy.Spider):
    name = 'bbc_articles'

    def __init__(self, start_urls=None, *args, **kwargs):
        super(BBC, self).__init__(*args, **kwargs)
        if start_urls is not None:
            self.start_urls = start_urls

    def parse(self, response):
        l = ItemLoader(item=ArticleItem(), response=response)
        l.add_xpath('title', '//h1[1]/text()')
        yield l.load_item()

    def process_body_text(self, paragraphs):
        processed_text = []

        for paragraph in paragraphs:
            paragraph_tree = etree.HTML(paragraph)

            paragraph_text = paragraph_tree.xpath('string()')

            processed_text.append(paragraph_text)

        return processed_text
