import httpx

from configs.settings import ConfigSettings
from models.base import Embedding
from models.web_pages import Embedding
from utils import logger

MODEL_NAMES = [
    'text-embedding-3-small',
    'text-embedding-3-large',
    'text-embedding-ada-002',
]


async def get_openai_embeddings(model_name, texts):
    if model_name not in MODEL_NAMES:
        raise Exception(f'Model does not exist: {model_name}')

    url = 'https://api.openai.com/v1/embeddings'

    data = {'model': model_name, 'input': [t['body'] for t in texts]}

    headers = {
        'Authorization': f"Bearer {ConfigSettings.openai_key}",
        'Content-Type': 'application/json',
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

        if response.status_code == 200:
            embeddings = response.json()
            if len(texts) == len(embeddings['data']):
                return embeddings
            else:
                logger.error('Texts and embeddings not equal')
        else:
            print(f"Error: {response.status_code}, {response.text}")


async def embed_batch(
    model_name: str, texts: list[str], batch_size: int = ConfigSettings.item_cache_limit
):
    article_embeddings = []
    for i in range(0, len(texts), batch_size):
        t = texts[i : i + batch_size]
        e = await get_openai_embeddings(model_name, t)
        article_embeddings.extend(e['data'])
    return article_embeddings
