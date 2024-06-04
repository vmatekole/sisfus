from datetime import date

import validators
from dateutil import parser
from scrapy.utils.test import get_crawler
from twisted.internet.defer import inlineCallbacks

from orchestration.prefect.authory_tasks import get_article_links_of_author
from scraper.articles import pipelines
from scraper.articles.spiders.bbc import BBC
from utils import logger

from .fixtures import (
    authory_article_list_response,
    bbc_future_article_response_body,
    bbc_future_article_url,
    setup_responses,
)


class TestAuthoryScraping:
    def test_get_authory_article_links_of_author(self):
        input = 'ZariaGorvett'

        result: list[str] = get_article_links_of_author(input)

        result = list(
            filter(
                lambda l: l
                == 'https://www.bbc.com/future/article/20150506-the-dark-psychology-of-voting',
                result,
            )
        )

        assert (
            result[0]
            == 'https://www.bbc.com/future/article/20150506-the-dark-psychology-of-voting'
        )

    def test_parsing_authory_article_links(authory_article_list_response):
        input = 'ZariaGorvett'

        result = get_article_links_of_author(input)
        assert validators.url(result[0])


class TestBBCArticleScraping:
    def test_bbc_future_article_scrape(self):
        pass

    # def test_bbc_future_article_local_scrape(
    #     self, setup_responses, bbc_future_article_response_body
    # ):
    #     spider = BBC()
    #     items = list(spider.parse(bbc_future_article_response_body))

    #     assert len(items) == 1
    #     assert items[0]['title'] == ["The 'dark earth' revealing the Amazon's secrets"]
    #     assert items[0]['body'] == ["The 'dark earth' revealing the Amazon's secrets"]
    #     assert items[0]['created_at'] == parser.parse('16th January 2024')

    @inlineCallbacks
    def test_bbc_future_article_local_scrape(
        self, setup_responses, bbc_future_article_response_body
    ):
        spider = BBC()
        items = list(spider.parse(bbc_future_article_response_body))

        pipeline_class = pipelines.ArticlePipeline

        crawler = get_crawler(BBC)
        pipe = pipeline_class.from_crawler(crawler)

        new_item = yield pipe.process_item(items[0], spider)

        assert len(items) == 1
        assert new_item['title'] == ["The 'dark earth' revealing the Amazon's secrets"]
        assert new_item['body'] == ["The 'dark earth' revealing the Amazon's secrets"]
        assert new_item['created_at'] == parser.parse('16th January 2024')
