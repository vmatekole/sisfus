import json
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from models.web_pages import Author
from sisfus.articles.spiders.bbc import BBC
from utils import logger


def get_source_article_list(response: str) -> list[str]:
    authory_articles: list[str] = []
    try:
        authory_reponse = json.loads(response)
        authory_articles = authory_reponse['articles']
        return authory_articles
    except json.JSONDecodeError as e:
        logger.exception(f'#F787h: {e}')
        raise


def run_bbc_spider():
    process = CrawlerProcess(get_project_settings())
    start_urls: list[str] = [
        'https://www.bbc.com/future/article/20240202-what-happened-to-the-codpiece',
        'https://www.bbc.com/future/article/20171127-the-buildings-designed-to-house-the-dead',
    ]

    process.crawl(BBC, start_urls=start_urls)
    process.start()
