import html

from w3lib.html import remove_tags

from utils import logger


def article_body(value):
    body: str = remove_tags(value)
    body = body.encode('raw_unicode_escape').decode('unicode_escape')
    return body


def source_name(value):
    return 'BBC'
