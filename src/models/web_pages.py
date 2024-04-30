import json
from datetime import datetime
from typing import Optional

import requests

from base.utils import logger
from models.base import WebPages


class Author(WebPages):
    first_name: str
    last_name: str

    @staticmethod
    def get_author_from_authory_article(a) -> 'Author':
        try:
            return Author(
                first_name=a['owner']['firstName'], last_name=a['owner']['lastName']
            )
        except json.JSONDecodeError as e:
            logger.exception(f'#rt577: {e}')
            raise

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Article(WebPages):
    author: Author
    title: str
    sourceUrl: str
    body: str
    created_at: Optional[datetime] = None
    modifed_at: Optional[datetime] = None
    tags: Optional[list[str]] = None

    @staticmethod
    def parse_source_article(originalUrl: str):
        return {'body': 'body', 'title': 'title'}


class Authory:
    @staticmethod
    def get_articles_of_author(author: str):
        response = requests.get(
            f'https://api-production.authory.com/content/{author}?take=300&collection=c5d1d6fb3283d4c4ba80a721ce88bcb26'
        )

        logger.debug(response)
        if response.status_code != 200:
            raise Exception(f'#565 Unable to get articles of {author}')

        articles: list[Article] = Authory.parse_articles(response.content)
        return articles

    @staticmethod
    def parse_articles(response: str):
        articles: list[Article] = []
        authory_articles = []
        try:
            authory_reponse = json.loads(response)
            authory_articles = authory_reponse['articles']
        except json.JSONDecodeError as e:
            logger.exception(f'#F787h: {e}')
            raise

        try:
            for a in authory_articles:
                s: dict[str, str] = Article.parse_source_article(a['originalUrl'])

                articles.append(
                    Article(
                        author=Author.get_author_from_authory_article(a),
                        title=s['title'],
                        sourceUrl=a['originalUrl'],
                        body=s['body'],
                    )
                )
            return articles
        except Exception as e:
            logger.exception(f'#ft: {e}')
            raise
