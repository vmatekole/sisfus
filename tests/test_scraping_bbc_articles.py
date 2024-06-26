import datetime
from unittest import mock

import pytest
import validators
from dateutil import parser
from scrapy.utils.test import get_crawler

from configs.settings import ConfigSettings
from models.web_pages import Article
from scraper import pipelines
from scraper.spiders.articles import BBC
from tasks.authory_tasks import get_article_links_of_author

from .fixtures import (
    authory_article_list_response,
    bbc_future_article_body_1,
    bbc_future_article_body_2,
    bbc_future_article_dict,
    bbc_future_article_response_body,
    bbc_future_article_url,
)


class TestAuthoryScraping:
    def test_get_authory_article_links_of_author(self):
        input = 'ZariaGorvett'

        result: list[str] = get_article_links_of_author(input)

        result = list(
            filter(
                lambda l: l
                == 'https://www.bbc.com/future/article/20240116-the-dark-earth-revealing-the-amazons-secrets',
                result,
            )
        )

        assert (
            result[0]
            == 'https://www.bbc.com/future/article/20240116-the-dark-earth-revealing-the-amazons-secrets'
        )

    def test_parsing_authory_article_links(authory_article_list_response):
        input = 'ZariaGorvett'

        result = get_article_links_of_author(input)
        assert validators.url(result[0])


class TestBBCArticleScraping:
    spider = BBC()

    def test_bbc_future_article_scrape(self):
        pass

    def test_bbc_future_article_local_scrape(
        self,
        bbc_future_article_response_body,
        bbc_future_article_body_1,
        bbc_future_article_body_2,
    ):
        spider = TestBBCArticleScraping.spider
        pipeline_class = pipelines.ArticleValidationPipeline
        pipe = pipeline_class.from_crawler(get_crawler(BBC))

        items = list(spider.parse(bbc_future_article_response_body))
        article: Article = pipe.process_item(items[0], spider)
        body = article.body

        assert len(items) == 1
        assert (
            article.source_url
            == 'https://www.bbc.com/future/article/20240116-the-dark-earth-revealing-the-amazons-secrets'
        )
        assert article.source_name == 'BBC'
        assert article.title == "The 'dark earth' revealing the Amazon's secrets"
        assert article.published_at == parser.parse('16th January 2024')
        assert bbc_future_article_body_1 in body
        assert bbc_future_article_body_2 in body

    @pytest.mark.skipif(
        ConfigSettings.test_without_bigquery,
        reason='No Bigquery available',
    )
    def test_bbc_future_article_bq_pipeline(self, bbc_future_article_dict):
        pipeline_class = pipelines.BigQueryArticlePipeline
        pipe = pipeline_class.from_crawler(get_crawler(BBC))
        spider = TestBBCArticleScraping.spider

        items = [Article(**bbc_future_article_dict)]
        new_item = yield pipe.process_item(items[0], spider)
        pipe.close_spider(spider)

        assert new_item.title == 'Satoshi Nakamoto is alive'
        assert pipe.cache_size == 0

    def test_bbc_future_article_mocked_bq_pipeline(
        self, mocker, bbc_future_article_dict
    ):

        pipeline_class = pipelines.BigQueryArticlePipeline
        pipe = pipeline_class.from_crawler(get_crawler(BBC))
        spider = TestBBCArticleScraping.spider

        expected_article = Article(
            title='Satoshi Nakamoto is alive',
            source_url='http://not.real',
            source_name='Source name',
            body='Body text',
            published_at=datetime.datetime(1980, 5, 22, 0, 0),
            updated_at=None,
            tags=None,
        )
        m = mock.Mock()
        pipe._bq_service.save_articles = m
        items = [Article(**bbc_future_article_dict)]
        new_item = pipe.process_item(items[0], spider)
        pipe.close_spider(spider)

        m.assert_called_once_with([expected_article])

        assert pipe.cache_size == 0
