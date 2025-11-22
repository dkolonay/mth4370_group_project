import os
import torch
import torch.nn as nn
from torchtext.vocab import GloVe

class WordEmbedding:
    def __init__(self, name: str = '840B', dim: int = 300):
        """
        Initializes the GloVe model and creates a PyTorch embedding layer.
        """

        cache_dir = os.path.abspath('../../data/cache')

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


# Example usage
if __name__ == "__main__":
    embedding_model = WordEmbedding(name='840B', dim=300)
    emb = embedding_model.get_embedding('king')
    print(emb)  # shape [1, 300]
