import scrapy
import scrapy.http
from rich import print
from scrapy import Spider


class BBC(Spider):
    name = 'bbc_articles'
    start_urls = ['https://authory.com/ZariaGorvett']

    def parse(self, response):
        article_titles = response.css('h2::text').getall()
        print(article_titles)
        # next_page_links = response.css(".next a")
        # yield from response.(article_titles, callback=self.parse_titles)
        # book_links = response.css("article a")
        # yield from response.follow_all(book_links, callback=self.parse_book)
