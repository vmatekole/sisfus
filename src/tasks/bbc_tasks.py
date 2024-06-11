import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from models.web_pages import Author
from scraper.spiders.articles import BBC

# def get_source_article_list(response: str) -> list[str]:
#     authory_articles: list[str] = []
#     try:
#         authory_reponse = json.loads(response)
#         authory_articles = authory_reponse['articles']
#         return authory_articles
#     except json.JSONDecodeError as e:
#         logger.exception(f'#F787h: {e}')
#         raise


def run_bbc_spider(urls):
    process = CrawlerProcess(get_project_settings())
    start_urls: list[str] = urls

    process.crawl(BBC, start_urls=start_urls)
    process.start()
