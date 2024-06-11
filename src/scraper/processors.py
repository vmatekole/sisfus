import html
import re

from w3lib.html import remove_tags


def article_body(value):
    body: str = remove_tags(value)
    body = body.encode('raw_unicode_escape').decode('unicode_escape')
    return body


def source_name(value):
    return 'BBC'


def parse_date(response):
    a = response.css('article')[0].get()
    article_txt = remove_tags(a)
    date_pattern = r'(?:\d{1,2})(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}'

    match = re.search(date_pattern, article_txt)
    return match.group()
