from datetime import datetime
from typing import Optional

from pydantic import field_serializer

from .base import Embedding


class Author:
    first_name: str
    last_name: str

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class TextChunk(Embedding):
    id: int
    text: str


class Article(Embedding):
    title: str
    body: str
    published_at: datetime
    updated_at: Optional[datetime] = None

    @field_serializer('published_at')
    def isodate(published_at):
        return published_at.isoformat()
