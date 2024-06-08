import pytest
from google.cloud import bigquery
from openai import embeddings

from services.bq import ArticleService, BqService
from tasks.embedding_tasks import create_article_embeddings

from .fixtures import bbc_future_article_dict, bbc_future_article_dict_1


class TestBQService:
    @pytest.mark.asyncio
    async def test_save_embedded_articles(
        self, bbc_future_article_dict, bbc_future_article_dict_1
    ):
        embeddings = await create_article_embeddings(
            'text-embedding-3-small',
            [bbc_future_article_dict, bbc_future_article_dict_1],
        )

        bq = ArticleService()

        bq.save_text_embeddings(embeddings)
