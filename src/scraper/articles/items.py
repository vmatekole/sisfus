import scrapy
from dateutil import parser
from itemloaders.processors import MapCompose, TakeFirst

from scraper.articles.utils import article_body


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    # sourceUrl: scrapy.Field
    # source_type: scrapy.Field
    body = scrapy.Field(
        input_processor=MapCompose(article_body), output_processor=TakeFirst()
    )
    created_at = scrapy.Field(
        input_processor=MapCompose(parser.parse), output_processor=TakeFirst()
    )
    # modifed_at: scrapy.Field
    # tags: scrapy.Field
