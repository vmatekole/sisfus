from datetime import datetime
from typing import Optional

from pydantic import field_serializer, model_serializer

from .base import WebPages


class Author(WebPages):
    first_name: str
    last_name: str

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Article(WebPages):
    title: str
    source_url: str
    source_name: str
    body: str
    published_at: datetime
    updated_at: Optional[datetime] = None
    tags: Optional[list[str]] = None

    @field_serializer('published_at')
    def isodate(published_at):
        return published_at.isoformat()


class ArticleEmbedding(WebPages):
    source_url: str
    embedding: list[float]

    @field_serializer('embedding')
    def embedding_to_str(embedding):
        embedding_str: list[str] = [str(e) for e in embedding]
        return ''.join(embedding_str)
