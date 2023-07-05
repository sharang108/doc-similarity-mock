import torch
from sentence_transformers import SentenceTransformer, util


class EmbeddingUtils:
    def __init__(self, prompt: str = None) -> None:
        self.model = SentenceTransformer("bert-base-nli-mean-tokens")
        self.prompt_embedding = (
            self.model.encode([prompt], convert_to_tensor=True) if prompt else None
        )

    def create_embeddings(self, documents: list) -> list[tuple]:
        embeddings = []
        for text in documents:
            encoding = self.model.encode([text])[0].tolist()
            embeddings.append((text, encoding))
        return embeddings

    def compare_embeddings(self, embeddings: list, threshold: float) -> dict:
        tensor_embeddings = [torch.tensor(embedding) for _, embedding in embeddings]
        similarity_scores = util.semantic_search(
            query_embeddings=self.prompt_embedding, corpus_embeddings=tensor_embeddings
        )
        max_result = {"score": 0, "text": ""}
        for result, (text, _) in zip(similarity_scores[0], embeddings):
            max_score = max_result.get("score")
            score = result["score"]
            if score >= threshold or score > max_score:
                max_result = {"score": score, "text": text}
        return max_result
