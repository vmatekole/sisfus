from models.web_pages import Article

from .fixtures import authory_content_response


class TestAuthoryScraping:
    def test_getting_authory_article_links(self, authory_content_response):
        input = authory_content_response

        result = Article.parse_authory_json(authory_content_response)

        assert isinstance(result[0], Article)
        assert (
            result[0].sourceUrl
            == 'https://www.bbc.com/future/article/20240202-what-happened-to-the-codpiece'
        )


class TestBBCArticleScraping:
    def test_bbc_future_article_scrape(self):
        pass
