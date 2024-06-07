import validators
from dateutil import parser
from orchestration.prefect.authory_tasks import get_article_links_of_author
from scrapy.utils.test import get_crawler
from twisted.internet.defer import inlineCallbacks

from models.web_pages import Article
from scraper.articles import pipelines
from scraper.articles.spiders.bbc import BBC
from utils import logger

from .fixtures import (
    authory_article_list_response,
    bbc_future_article_body_1,
    bbc_future_article_body_2,
    bbc_future_article_dict,
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
    spider = BBC()

    def test_bbc_future_article_scrape(self):
        pass

    @inlineCallbacks
    def test_bbc_future_article_local_scrape(
        setup_responses,
        bbc_future_article_response_body,
        bbc_future_article_body_1,
        bbc_future_article_body_2,
    ):
        spider = TestBBCArticleScraping.spider
        pipeline_class = pipelines.ArticleValidationPipeline
        pipe = pipeline_class.from_crawler(get_crawler(BBC))

        items = list(spider.parse(bbc_future_article_response_body))

        article: Article = yield pipe.process_item(items[0], spider)
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

    @inlineCallbacks
    def test_bbc_future_article_bq_pipeline(setup_responses, bbc_future_article_dict):
        pipeline_class = pipelines.BigQueryArticlePipeline
        pipe = pipeline_class.from_crawler(get_crawler(BBC))
        spider = TestBBCArticleScraping.spider

        items = [Article(**bbc_future_article_dict)]

        new_item = yield pipe.process_item(items[0], spider)
