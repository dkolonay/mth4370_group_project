import os
import pickle
import torch
import torch.nn.functional as F
import faiss
from typing import List, Optional, Union

class MovieRecommender:
    """
    Movie recommendation system using FAISS for fast similarity search

    Supports:
    - Movie-to-movie similarity
    - Text query search
    - Multi-movie input
    - Hybrid (movies + text)
    """

    def __init__(self, sbert_encoder, embeddings_path="data/processed/embeddings.pt", mappings_path="data/processed/mappings_no_dataset.pkl"):
        """
        Args:
        	sbert_encoder: MPNetEncoder instance for text queries
            embeddings_path: Path to embeddings .pt file (from generate_embeddings.py)
            mappings_path: Path to mappings.pkl
        """
        if not os.path.exists(embeddings_path):
            raise ValueError("embeddings are required.")

        #load embeddings
        embeddings_dict = torch.load(embeddings_path)

        self.fused_embeddings = embeddings_dict.get('fused')
        self.text_embeddings = embeddings_dict.get('text_only')

        self.num_movies, self.embed_dim = self.fused_embeddings.shape

        # Load mappings
        with open(mappings_path, 'rb') as f:
            self.mappings = pickle.load(f)

        self.tmdb_to_idx = self.mappings['tmdb_to_idx']
        self.idx_to_tmdb = {v: k for k, v in self.tmdb_to_idx.items()}

        # Text encoder
        self.sbert = sbert_encoder

        # Build FAISS indices
        self.fused_index = self._build_faiss_index(self.fused_embeddings)
        self.text_index = self._build_faiss_index(self.text_embeddings)

    def _build_faiss_index(self, embeddings):
        """Build FAISS index for fast similarity search"""
        embeddings_np = embeddings.cpu().numpy().astype('float32')
        faiss.normalize_L2(embeddings_np)

        # Use IndexFlatIP (Inner Product) for cosine similarity on normalized vectors
        index = faiss.IndexFlatIP(embeddings_np.shape[1])
        index.add(embeddings_np)

        return index

    def search_by_movie_ids(self, movie_ids: Union[int, List[int]], k: int = 10,
                           exclude_input: bool = True) -> List[dict]:
        """
        Find similar movies based on one or more input movies

        Args:
            movie_ids: Single TMDB ID or list of TMDB IDs
            k: Number of recommendations
            exclude_input: Don't return the input movies in results

        Returns:
            List of dicts with movie info and similarity scores

        Example:
            >> recommender.search_by_movie_ids(603, k=5)
            >> recommender.search_by_movie_ids([27205, 157336], k=10)
        """
        if isinstance(movie_ids, int): # singel movie_id
            movie_ids = [movie_ids]

        # Get embeddings for input movies
        indices = [self.tmdb_to_idx[id] for id in movie_ids if id in self.tmdb_to_idx]

        if not indices:
            raise ValueError(f"No valid movie IDs found in: {movie_ids}")

        # Average embeddings if multiple movies
        query_embedding = self.fused_embeddings[indices].mean(dim=0, keepdim=True)

        # Normalize
        query_embedding = F.normalize(query_embedding, p=2, dim=1) #l2 norm
        query_np = query_embedding.cpu().numpy().astype('float32')

        # Search (get extra results if excluding input)
        num_results = k + len(indices) if exclude_input else k
        scores, result_indices = self.fused_index.search(query_np, num_results)

        # Convert to results
        results = []
        for score, idx in zip(scores[0], result_indices[0]):
            if exclude_input and idx in indices:
                continue

            tmdb_id = self.idx_to_tmdb[idx]
            results.append(tmdb_id)

            if len(results) >= k:
                break

        return results

    def search_by_text(self, query: str, k: int = 10) -> List[dict]:
        """
        Find movies based on text query

        Args:
            query: Natural language query like "sci-fi movies about AI"
            k: Number of recommendations

        Returns:
            List of dicts with movie info and similarity scores

        Example:
            >> recommender.search_by_text("cyberpunk action with philosophy")
        """
        # Encode text query
        with torch.no_grad():
            query_emb = self.sbert.encode(query).unsqueeze(0)

        # Normalize
        query_emb = F.normalize(query_emb, p=2, dim=1) #l2 norm
        query_np = query_emb.cpu().numpy().astype('float32')

        # Search
        scores, result_indices = self.text_index.search(query_np, k)

        # Convert to results
        results = []
        for score, idx in zip(scores[0], result_indices[0]):
            tmdb_id = self.idx_to_tmdb[idx]
            results.append(tmdb_id)

        return results

    def search_hybrid(self, movie_ids: Optional[Union[int, List[int]]] = None,
                     text_query: Optional[str] = None,
                     movie_weight: float = 0.5,
                     k: int = 10) -> List[dict]:
        """
        Hybrid search: combine movie similarity and text query

        Args:
            movie_ids: Single TMDB ID or list (optional)
            text_query: Text description (optional)
            movie_weight: Weight for movie embeddings (0 to 1)
            k: Number of recommendations

        Returns:
            List of dicts with movie info and similarity scores

        Example:
            >> recommender.search_hybrid(
            ...     movie_ids=550,
            ...     text_query="but with a clif hanger",
            ...     movie_weight=0.7
            ... )
        """
        if movie_ids is None and text_query is None:
            raise ValueError("Must provide either movie_ids or text_query")

        embeddings_to_combine = []
        weights = []

        # Add movie embeddings
        if movie_ids is not None:
            if isinstance(movie_ids, int):
                movie_ids = [movie_ids]

            indices = [self.tmdb_to_idx[mid] for mid in movie_ids if mid in self.tmdb_to_idx]
            if indices:
                movie_emb = self.fused_embeddings[indices].mean(dim=0, keepdim=True)
                embeddings_to_combine.append(movie_emb)
                weights.append(movie_weight)

        # Add text embedding
        if text_query is not None:
            with torch.no_grad():
                text_emb = self.sbert.encode(text_query).unsqueeze(0)

            # Project to same embedding space
            if text_emb.shape[1] != self.embed_dim:
                # Simple padding/truncation
                if text_emb.shape[1] < self.embed_dim:
                    text_emb = F.pad(text_emb, (0, self.embed_dim - text_emb.shape[1]))
                else:
                    text_emb = text_emb[:, :self.embed_dim]

            embeddings_to_combine.append(text_emb)
            weights.append(1 - movie_weight)

        # Weighted combination
        qstacked = torch.stack([w * emb for w, emb in zip(weights, embeddings_to_combine)])
        query_embedding = torch.sum(qstacked, dim=0)
        query_embedding = F.normalize(query_embedding, p=2, dim=1)

        # Search
        query_np = query_embedding.cpu().numpy().astype('float32')
        scores, result_indices = self.fused_index.search(query_np, k)

        # Convert to results
        results = []
        for score, idx in zip(scores[0], result_indices[0]):
            tmdb_id = self.idx_to_tmdb[idx]
            results.append(tmdb_id)

        return results
