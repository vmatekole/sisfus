from cgitb import text
from io import text_encoding

import httpx
from rich import print_json

from configs.settings import ConfigSettings
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
            r = []
            if len(texts) == len(embeddings['data']):
                for i, a in enumerate(texts):
                    r.append(texts[i])
                    r[i]['embedding'] = embeddings['data'][i]['embedding']
                return r
            else:
                logger.error('Texts and embeddings not equal')
        else:
            print(f"Error: {response.status_code}, {response.text}")


async def create_embeddings(model_name, texts):
    article_embeddings = []
    for i in range(0, len(texts), 100):
        c = texts[i : i + 100]
        article_embeddings.extend(await get_openai_embeddings(model_name, c))

    return article_embeddings
