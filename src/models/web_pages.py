import json
from datetime import datetime
from turtle import title
from typing import Optional

from base.utils import logger
from models.base import WebPages


class Author(WebPages):
    firstName: str
    lastName: str

    @staticmethod
    def get_author_from_authory_article(a) -> 'Author':
        try:
            return Author(
                firstName=a['owner']['firstName'], lastName=a['owner']['lastName']
            )
        except json.JSONDecodeError as e:
            logger.exception(f'#rt577: {e}')
            raise


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

    @staticmethod
    def parse_authory_json(response: str):
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
