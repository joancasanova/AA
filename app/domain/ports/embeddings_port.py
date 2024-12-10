# domain/ports/embeddings_port.py

class EmbeddingsPort:
    def get_similarity(self, text1: str, text2: str) -> float:
        raise NotImplementedError
