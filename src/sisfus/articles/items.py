import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    sourceUrl: scrapy.Field
    source_type: scrapy.Field
    body: scrapy.Field
    created_at: scrapy.Field
    modifed_at: scrapy.Field
    tags: scrapy.Field
