import os
import torch
import torch.nn as nn
import re
from torchtext.vocab import GloVe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

class WordEmbedding:
    def __init__(self, name: str = '840B', dim: int = 300):
        """
        Initializes the GloVe model and creates a PyTorch embedding layer.
        """
        cache_dir = os.path.join(PROJECT_ROOT, "data", "cache")

        self.glove = GloVe(name=name, dim=dim, cache=cache_dir)

        weights = self.glove.vectors  # [vocab_size, embedding_dim]
        self.embedding_layer = nn.Embedding.from_pretrained(weights)

        self.stoi = self.glove.stoi

    def get_embedding(self, word: str) -> torch.Tensor:
        """
        Returns the embedding tensor for a given word.
        """
        if word not in self.stoi:
            raise ValueError(f"Word '{word}' not in vocabulary.")

        word_index = torch.LongTensor([self.stoi[word]])
        return self.embedding_layer(word_index)

    def split_keywords(self, x):
        """
        Splits strings of keywords into words, also singular words.
        """
        if not x or str(x).strip().lower() == "nan":
            return []

        keywords = []
        for kw in x.split(","):
            kw = kw.strip().lower()
            if not kw:
                continue

            # Remove anything in parentheses
            kw = re.sub(r"\(.*?\)", "", kw)

            # Remove punctuation
            kw = re.sub(r"[^\w\s]", "", kw)  # keep letters, numbers, underscores, spaces

            # Split multi-word phrases into individual words
            words = kw.split()

            words = [w.strip() for w in words if w.strip() in self.stoi]

            keywords.extend(words)

        return keywords


# Example usage
if __name__ == "__main__":
    embedding_model = WordEmbedding(name='840B', dim=300)
    emb = embedding_model.get_embedding('king')
    print(emb)  # shape [1, 300]
