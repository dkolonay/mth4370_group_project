import torch
import torch.nn as nn
import torch.nn.functional as F

class MovieFusionModel(nn.Module):
    """
    Multi-modal fusion model with attention mechanism
    Combines text, keywords, genres, images, and metadata into a single embedding
    """
    def __init__(self, output_dim=512):
        super().__init__()
        self.output_dim = output_dim

        # Project all features to same dimension (256)
        self.text_proj = nn.Linear(768, 256)
        self.keyword_proj = nn.Linear(300, 256)
        self.genre_proj = nn.Linear(19, 256)
        self.poster_proj = nn.Linear(512, 256)
        self.backdrop_proj = nn.Linear(512, 256)

        # Metadata: 7 scalars (year, month_sin, month_cos, vote_avg, vote_count, popularity, runtime)
        self.meta_proj = nn.Linear(7, 256)

        # Attention mechanism
        self.attention = nn.Sequential(
            nn.Linear(256, 128),
            nn.Tanh(),
            nn.Linear(128, 1)
        )

        # Final embedding head
        self.head = nn.Sequential(
            nn.Linear(256, output_dim),
            nn.LayerNorm(output_dim)
        )

    def forward(self, features):
        """
        Args:
            features: dict with keys from features.pt
                - text: [batch, 768]
                - keywords: [batch, 300]
                - genres: [batch, 19]
                - poster_file: [batch, 512]
                - backdrop_file: [batch, 512]
                - year, month_sin, month_cos, vote_average, vote_count, popularity, runtime: [batch, 1]
                - mask: [batch, 12]

        Returns:
            embeddings: [batch, output_dim] L2-normalized embeddings
        """
        # Project all modalities to 256-dim
        emb_text = torch.tanh(self.text_proj(features['text']))
        emb_keywords = torch.tanh(self.keyword_proj(features['keywords']))
        emb_genres = torch.tanh(self.genre_proj(features['genres']))
        emb_poster = torch.tanh(self.poster_proj(features['poster_file']))
        emb_backdrop = torch.tanh(self.backdrop_proj(features['backdrop_file']))

        # Combine scalar features
        scalars = torch.cat([
            features['year'],
            features['month_sin'],
            features['month_cos'],
            features['vote_average'],
            features['vote_count'],
            features['popularity'],
            features['runtime']
        ], dim=1)
        emb_meta = torch.tanh(self.meta_proj(scalars))

        # Stack: [batch, 6 modalities, 256]
        stack = torch.stack([
            emb_text,
            emb_keywords,
            emb_genres,
            emb_poster,
            emb_backdrop,
            emb_meta
        ], dim=1)

        modality_mask = torch.stack([
            features['mask'][:, 0],   # text
            features['mask'][:, 1],   # keywords
            features['mask'][:, 2],   # genres
            features['mask'][:, 10],  # poster
            features['mask'][:, 11],  # backdrop
            torch.all(features['mask'][:, 3:10] > 0, dim=1).float()  # meta (all scalars present)
        ], dim=1).unsqueeze(-1)  # [batch, 6, 1]

        # Calculate attention scores
        attn_scores = self.attention(stack)  # [batch, 6, 1]

        # Mask out missing modalities (set to -inf so softmax makes them 0)
        min_value = torch.finfo(attn_scores.dtype).min
        attn_scores = attn_scores.masked_fill_(modality_mask == 0, min_value)

        # Normalize to get weights
        attn_weights = F.softmax(attn_scores, dim=1)

        # Weighted sum
        fused = (stack * attn_weights).sum(dim=1)  # [batch, 256]

        # Final projection
        embedding = self.head(fused)  # [batch, output_dim]

        # L2 normalize for cosine similarity
        return F.normalize(embedding, p=2, dim=1)
