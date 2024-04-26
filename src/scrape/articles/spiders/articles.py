import scrapy
import scrapy.http
from lxml import etree
from rich import print
from scrapy import Spider


class BBC(Spider):
    name = 'bbc_articles'
    start_urls = [
        'https://www.bbc.com/future/article/20240202-what-happened-to-the-codpiece'
    ]

    def parse(self, response):
        yield from response.follow_all(
            [
                'https://www.bbc.com/future/article/20240202-what-happened-to-the-codpiece'
            ],
            callback=self.parse_bbc_future_article,
        )

    def parse_bbc_future_article(self, response):
        paragraphs = response.css(
            '.article__body-content .body-text-card__text p'
        ).getall()
        paragraphs = self.process_body_text(paragraphs)

        yield {
            'title': response.css('.article__body-content .article__intro::text').get(),  # type: ignore
            'body': paragraphs,
        }

    def process_body_text(self, paragraphs):
        processed_text = []

        for paragraph in paragraphs:
            paragraph_tree = etree.HTML(paragraph)

            paragraph_text = paragraph_tree.xpath('string()')

            processed_text.append(paragraph_text)

        return processed_text
