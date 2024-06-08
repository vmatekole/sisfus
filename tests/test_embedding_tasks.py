import pytest

from tasks.embedding_tasks import create_article_embeddings

from .fixtures import bbc_future_article_dict, bbc_future_article_dict_1


class TestEmbeddingTasks:
    @pytest.mark.asyncio
    async def test_open_ai_embedding(
        self, bbc_future_article_dict, bbc_future_article_dict_1
    ):
        text_embeddings = await create_article_embeddings(
            'text-embedding-3-small',
            [bbc_future_article_dict, bbc_future_article_dict_1],
        )

        expected_slice_1 = [
            0.017624648,
            0.039582975,
            0.013222301,
            0.027787432,
            -0.021546323,
            -0.0064661857,
        ]
        expected_slice_2 = [
            0.027645022,
            0.020165363,
            0.005025193,
            0.0116005745,
            -0.009772644,
            -0.039891507,
        ]

        assert (
            expected_slice_1 == text_embeddings[0].embedding[0 : len(expected_slice_1)]
        )
        assert (
            expected_slice_2 == text_embeddings[1].embedding[0 : len(expected_slice_2)]
        )
