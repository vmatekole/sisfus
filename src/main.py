from tasks.authory_tasks import get_article_links_of_author
from tasks.bbc_tasks import run_bbc_spider
from utils import logger

if __name__ == '__main__':
    urls: list[str] = get_article_links_of_author('ZariaGorvett')
    run_bbc_spider(urls)
