from unittest import result

import requests

from base.utils import logger
from models.web_pages import Article, Authory

from .fixtures import authory_content_response


class TestAuthoryScraping:
    def test_get_authory_article_links_of_author(self):
        input = 'ZariaGorvett'

        result: list[str] = Authory.get_article_links_of_author(input)

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

    def test_parsing_authory_article_links(self, authory_content_response):
        input = authory_content_response

        result: list[Article] = Authory.parse_articles(authory_content_response)

        assert isinstance(result[0], Article)
        assert (
            result[0].sourceUrl
            == 'https://www.bbc.com/future/article/20240202-what-happened-to-the-codpiece'
        )


class TestBBCArticleScraping:
    def test_bbc_future_article_scrape(self):
        pass
