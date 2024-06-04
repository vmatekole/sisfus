import json
from datetime import datetime
from typing import Optional

import requests

from utils import logger

from .base import WebPages


class Author(WebPages):
    first_name: str
    last_name: str

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Article(WebPages):
    title: str
    body: str
    created_at: Optional[datetime]
    modifed_at: Optional[datetime] = None
    tags: Optional[list[str]] = None
