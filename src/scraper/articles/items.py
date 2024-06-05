import scrapy
from dateutil import parser
from itemloaders.processors import MapCompose, TakeFirst

from scraper.articles.processors import article_body, source_name


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    source_url = scrapy.Field()
    source_name = scrapy.Field(
        input_processor=MapCompose(source_name), output_processor=TakeFirst()
    )
    body = scrapy.Field(
        input_processor=MapCompose(article_body), output_processor=TakeFirst()
    )
    created_at = scrapy.Field(
        input_processor=MapCompose(parser.parse), output_processor=TakeFirst()
    )
