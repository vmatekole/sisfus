from typing import Optional

from pydantic import BaseModel, field_serializer


class MetaDocument(BaseModel):
    source_url: str
    source_name: str
    tags: Optional[list[str]] = None


class Embedding(MetaDocument):
    embedding: Optional[list[float]] = None

    @field_serializer('embedding')
    def embedding_to_str(embedding):
        embedding_str: list[str] = [str(e) for e in embedding]
        return ''.join(embedding_str)
