import json
import sys

import requests
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from base.utils import logger
from models.web_pages import Author
from sisfus.articles.spiders.bbc import BBC


def _request_authory_author(author) -> requests.Response:
    response: requests.Response = requests.get(
        f'https://api-production.authory.com/content/{author}?take=300&collection=c5d1d6fb3283d4c4ba80a721ce88bcb26'
    )

    if response.status_code != 200:
        raise Exception(f'#565 Unable to get articles of {author}')
    return response


def get_author_from_authory_article(a) -> Author:
    try:
        return Author(
            first_name=a['owner']['firstName'], last_name=a['owner']['lastName']
        )
    except json.JSONDecodeError as e:
        logger.exception(f'#rt577: {e}')
        raise


def get_article_links_of_author(author: str) -> list[str]:
    response: requests.Response = _request_authory_author(author)

    articles = json.loads(response.content)['articles']
    return [a['originalUrl'] for a in articles]
