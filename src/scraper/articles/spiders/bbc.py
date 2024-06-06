import scrapy
from scrapy.loader import ItemLoader

from scraper.articles.items import ArticleItem

from ..processors import source_name


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
        l.add_css('title', 'article h1:first-of-type::text')
        l.add_css('published_at', 'article time::text')
        l.add_css('body', 'article')
        yield l.load_item()
