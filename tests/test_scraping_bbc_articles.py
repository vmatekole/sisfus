import os
from unittest.mock import MagicMock, patch

import pytest
import requests
import responses
import scrapy
import validators
from scrapy.crawler import Crawler, CrawlerProcess, CrawlerRunner
from scrapy.http.response.html import HtmlResponse
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import defer

from authory_tasks import get_article_links_of_author
from base.utils import logger
from models.web_pages import Article
from sisfus.articles.spiders.bbc import BBC

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

    def test_bbc_future_article_local_scrape(
        self, setup_responses, bbc_future_article_response_body
    ):
        spider = BBC()
        items = list(spider.parse(bbc_future_article_response_body))

        assert len(items) == 1
        assert items[0]['title'] == ["The 'dark earth' revealing the Amazon's secrets"]
