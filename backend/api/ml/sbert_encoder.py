import torch.nn as nn
from sentence_transformers import SentenceTransformer

class MPNetEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        self.output_dim = 768

    def forward(self, texts):
        return self.model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)

class MiniLMEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.output_dim = 384

    def forward(self, texts):
        return self.model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)