import os

import pytest
import responses
from dateutil import parser
from scrapy.http import HtmlResponse, Request


@pytest.fixture
def bbc_future_article_url():
    return 'https://www.bbc.com/future/article/20240116-the-dark-earth-revealing-the-amazons-secrets'


@pytest.fixture
def bbc_future_article_body_1():
    return 'Amid the discovery of a lost city in the Amazon rainforest, scientists'


@pytest.fixture
def bbc_future_article_body_2():
    return (
        'Now businesses are attempting to capitalise on this ancient method, in'
        ' a quest to help farmers to improve their soil and combat climate'
        ' change at the same time.'
    )


@pytest.fixture
def bbc_future_article_dict():
    return {
        'body': 'Article body',
        'title': 'Title',
        'source_url': 'http://not.real',
        'source_name': 'Source name',
        'body': 'Body',
        'published_at': parser.parse('22nd May 1980'),
    }


@pytest.fixture
def bbc_future_article_response_body(bbc_future_article_url) -> HtmlResponse:
    file_path: str = os.path.join(
        os.path.dirname(__file__), 'data/html', 'bbc-future-28-05-2024.html'
    )
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    response = HtmlResponse(
        url=bbc_future_article_url,
        request=Request(url=bbc_future_article_url),
        body=file_content,
        encoding='utf-8',
    )
    return response


@pytest.fixture
def authory_article_list_response():
    return r""" {
  "articles": [
    {
      "type": "Article",
      "title": "How the codpiece flopped",
      "owner": {
        "slug": "ZariaGorvett",
        "firstName": "Zaria",
        "lastName": "Gorvett",
        "avatarUrl": [
          {
            "url": "https://profile-images-production.authory.com/ZariaGorvett/avatar_beec4960a1ee799ccc8d75e80f9cbf97303d4d99536a8ebc8d995dd3e48e71b6_300_300.jpg",
            "width": 300,
            "height": 300
          }
        ],
        "assetKey": "ZariaGorvett"
      },
      "description": "Some codpieces were empty – while others were used to store potpourri. Some time around 1536, Hans Holbein the Younger was finessing Henry VIII's crotch. With a fine brush in his hand and a palette of watercolour paints beside him, the master artist…",
      "sourceName": "BBC",
      "source": "bbc.com",
      "sourceType": "Web",
      "date": "2024-02-04T10:00:00+00:00",
      "slug": null,
      "canonicalSlug": null,
      "textLength": 9573,
      "originalUrl": "https://www.bbc.com/future/article/20240202-what-happened-to-the-codpiece",
      "publishedOnAuthory": false,
      "pinned": false,
      "public": false,
      "effectiveVisibility": "preview",
      "wordCount": 1568,
      "thumbnailImage": "https://images-production.authory.com/ZariaGorvett/edf2e7b1-244c-46a7-adea-1b4bf332a7f1/thumbnail_c3221630-c8de-11ee-a565-ff7de313b796.webp",
      "previewImage": "https://images-production.authory.com/ZariaGorvett/edf2e7b1-244c-46a7-adea-1b4bf332a7f1/preview_c3221630-c8de-11ee-a565-ff7de313b796.webp",
      "previewImageCenterX": 1080,
      "previewImageCenterY": 0,
      "previewImageHeight": 1079,
      "previewImageWidth": 1920,
      "snippetOnly": false,
      "collections": []
    },
    {
      "type": "Article",
      "title": "Sleep tight: A curious history of beds through the centuries",
      "owner": {
        "slug": "ZariaGorvett",
        "firstName": "Zaria",
        "lastName": "Gorvett",
        "avatarUrl": [
          {
            "url": "https://profile-images-production.authory.com/ZariaGorvett/avatar_beec4960a1ee799ccc8d75e80f9cbf97303d4d99536a8ebc8d995dd3e48e71b6_300_300.jpg",
            "width": 300,
            "height": 300
          }
        ],
        "assetKey": "ZariaGorvett"
      },
      "description": "From beds for Roman newlyweds, to \"hangover\" benches for 19th-Century workers: the pursuit of a good night's sleep has followed us through the ages. Amid the windswept expanse of the Bay of Skaill, on the west coast of the Scottish island of Orkney,…",
      "sourceName": "BBC",
      "source": "bbc.com",
      "sourceType": "Web",
      "date": "2024-01-28T12:05:00+00:00",
      "slug": null,
      "canonicalSlug": null,
      "textLength": 9346,
      "originalUrl": "https://www.bbc.com/future/article/20240126-sleep-tight-a-curious-history-of-beds-through-the-centuries",
      "publishedOnAuthory": false,
      "pinned": false,
      "public": false,
      "effectiveVisibility": "preview",
      "wordCount": 1553,
      "thumbnailImage": "https://images-production.authory.com/ZariaGorvett/8355d7cd-c381-4006-a078-15a5b054fb29/thumbnail_a47d6400-c8de-11ee-a565-ff7de313b796.webp",
      "previewImage": "https://images-production.authory.com/ZariaGorvett/8355d7cd-c381-4006-a078-15a5b054fb29/preview_a47d6400-c8de-11ee-a565-ff7de313b796.webp",
      "previewImageCenterX": 960,
      "previewImageCenterY": 505,
      "previewImageHeight": 1079,
      "previewImageWidth": 1920,
      "snippetOnly": false,
      "collections": []
    },
    {
      "type": "Article",
      "title": "The strange reasons medieval people slept in cupboards",
      "owner": {
        "slug": "ZariaGorvett",
        "firstName": "Zaria",
        "lastName": "Gorvett",
        "avatarUrl": [
          {
            "url": "https://profile-images-production.authory.com/ZariaGorvett/avatar_beec4960a1ee799ccc8d75e80f9cbf97303d4d99536a8ebc8d995dd3e48e71b6_300_300.jpg",
            "width": 300,
            "height": 300
          }
        ],
        "assetKey": "ZariaGorvett"
      },
      "description": "These cosy, wardrobe-like pieces of furniture could reportedly sleep up to five people. Why did they fall out of fashion? At a museum in Wick, in the far north of Scotland, is what looks like a particularly large pine wardrobe. With a pair of…",
      "sourceName": "BBC",
      "source": "bbc.com",
      "sourceType": "Web",
      "date": "2024-01-22T14:00:00+00:00",
      "slug": null,
      "canonicalSlug": null,
      "textLength": 5210,
      "originalUrl": "https://www.bbc.com/future/article/20240122-the-strange-reasons-medieval-people-slept-in-cupboards",
      "publishedOnAuthory": false,
      "pinned": false,
      "public": false,
      "effectiveVisibility": "preview",
      "wordCount": 893,
      "thumbnailImage": "https://images-production.authory.com/ZariaGorvett/32331c1b-7bb8-4157-9beb-291a941c2cc1/thumbnail_9eaf2f40-c8de-11ee-a565-ff7de313b796.webp",
      "previewImage": "https://images-production.authory.com/ZariaGorvett/32331c1b-7bb8-4157-9beb-291a941c2cc1/preview_9eaf2f40-c8de-11ee-a565-ff7de313b796.webp",
      "previewImageCenterX": 1560,
      "previewImageCenterY": 843,
      "previewImageHeight": 1080,
      "previewImageWidth": 1920,
      "snippetOnly": false,
      "collections": []
    }
  ],
  "typeCounts": {
    "Article": 197,
    "VideoPost": 0,
    "TextPost": 0,
    "ImagePost": 0,
    "ReplyPost": 0,
    "PodcastItem": 0,
    "PdfFile": 0,
    "Video": 0,
    "Thread": 0,
    "Website": 0,
    "Email": 0
  },
  "filteredCount": 197,
  "pinned": null,
  "oldestArticleDate": "2015-05-06T00:00:00+00:00"
}"""


@pytest.fixture
def setup_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
