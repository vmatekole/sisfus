import scrapy
from dateutil import parser
from itemloaders.processors import MapCompose, TakeFirst

from scraper.articles.processors import article_body, source_name


class ArticleItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    source_url = scrapy.Field(output_processor=TakeFirst())
    source_name = scrapy.Field(
        input_processor=MapCompose(source_name), output_processor=TakeFirst()
    )
    body = scrapy.Field(
        input_processor=MapCompose(article_body), output_processor=TakeFirst()
    )
    published_at = scrapy.Field(
        input_processor=MapCompose(parser.parse), output_processor=TakeFirst()
    )
