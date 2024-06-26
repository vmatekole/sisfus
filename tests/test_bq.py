import pytest
from google.cloud import bigquery

from client.bq import Bq
from services.bq import ArticleService, BqService
from tasks.embedding_tasks import embed_batch

from .fixtures import bbc_future_article_dict, bbc_future_article_dict_1


# TODO: Look at mocking bigquery.Client().
class TestBQService:
    @pytest.mark.skip(reason='might do away with ArticleEmbeddings entirely')
    @pytest.mark.asyncio
    async def test_save_embedded_articles(
        self, mocker, bbc_future_article_dict, bbc_future_article_dict_1
    ):
        embeddings = await embed_batch(
            'text-embedding-3-small',
            [bbc_future_article_dict, bbc_future_article_dict_1],
        )

        # TODO Make more robust and check rows persisted
        bq_service = ArticleService()
        committed = bq_service.save_text_embeddings(embeddings)
        assert committed == True
