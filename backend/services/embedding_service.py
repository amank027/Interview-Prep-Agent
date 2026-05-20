from fastembed import TextEmbedding


class EmbeddingService:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self._model = TextEmbedding(model_name=model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [emb.tolist() for emb in self._model.embed(texts)]

    def embed_single(self, text: str) -> list[float]:
        return self.embed([text])[0]
