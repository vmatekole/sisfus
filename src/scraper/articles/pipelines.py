# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from utils import logger


class ArticlePipeline:
    def process_item(self, item, spider):
        title = item['title'][0]
        body = item['body'].replace(title, '')
        item['body'] = body
        return item

    @classmethod
    def from_crawler(cls, crawler):
        try:
            pipe = cls.from_settings(crawler.settings)  # type: ignore[attr-defined]
        except AttributeError:
            pipe = cls()
        pipe.crawler = crawler
        pipe._fingerprinter = crawler.request_fingerprinter
        return pipe
