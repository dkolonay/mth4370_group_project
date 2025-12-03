import os
import pickle
import re
from typing import Optional

import pandas as pd
import torch
from PIL import Image
from torchvision.transforms import InterpolationMode
from tqdm import tqdm

from ml.src.processing.cnn_encoder import ResNet50Encoder
from ml.src.processing.keywords_encoder import WordEmbedding
from ml.src.processing.sbert_encoder import MPNetEncoder

from torchvision import transforms

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DIR = os.path.join(PROJECT_ROOT, "data", "processed")

FEATURE_IDX = {
    "text": 0,
    "keywords": 1,
    "genres": 2,
    "year": 3,
    "month_sin": 4,
    "month_cos": 5,
    "vote_average": 6,
    "vote_count": 7,
    "popularity": 8,
    "runtime": 9,
    "poster": 10,
    "backdrop": 11
}

ALL_GENRES = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama',
    'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance',
    'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
]

GENRE_IDX = {genre: i for i, genre in enumerate(ALL_GENRES)}

def clean_text(x):
    # 1. Handle missing or nan
    if pd.isna(x) or not x or str(x).lower() == "nan":
        return ""

    text = str(x)

    # 2. Remove weird whitespace
    text = text.replace("\n", " ").replace("\t", " ")

    # 3. Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    # 4. Remove duplicate punctuation
    text = re.sub(r"[.]{2,}", ".", text)
    text = re.sub(r"[,]{2,}", ",", text)
    text = re.sub(r"[!]{2,}", "!", text)
    text = re.sub(r"[?]{2,}", "?", text)

    # 5. Strip leading/trailing spaces & punctuation
    return text.strip().strip(".")

def get_text_features(movie_item, sbert_encoder) -> Optional[torch.Tensor]:
    title = clean_text(movie_item.get("title"))
    tagline = clean_text(movie_item.get("tagline"))
    overview = clean_text(movie_item.get("overview"))

    parts = []
    if title:
        parts.append(f"{title}.")
    if tagline:
        parts.append(f"{tagline}.")
    if overview:
        parts.append(f"{overview}.")

    text = " ".join(parts)

    if not text:
        return None

    with torch.no_grad():
        embedding = sbert_encoder.encode(text)  # if its empty sbert will just give it a default encoding
    return embedding.cpu()

def precompute_keywords(movie_item, words : WordEmbedding) -> Optional[torch.Tensor]:
    keywords_raw = movie_item.get("keywords")

    # Check for NaN before passing to split_keywords
    if pd.isna(keywords_raw) or not keywords_raw:
        return None

    keywords = words.split_keywords(keywords_raw) # makes sure keywords are in glove 840b.300d

    if not keywords:
        return None

    embeddings = [words.get_embedding(keyword) for keyword in keywords]

    if not embeddings:
        return None

    embeddings_tensor = torch.vstack(embeddings)  # shape: [len(words), 300]
    pooled_embedding = embeddings_tensor.mean(dim=0)  # shape: [300]
    return pooled_embedding

def one_hot_encode_genres(movie_item) -> Optional[torch.Tensor]:
    movie_genres = movie_item.get('genres')

    if pd.isna(movie_genres) or not movie_genres:
        return None

    movie_genres = [g.strip() for g in movie_genres.split(',') if g.strip()]

    movie_genre_features = torch.zeros(len(GENRE_IDX), dtype=torch.float32)
    for g in movie_genres:
        if g in GENRE_IDX:
            movie_genre_features[GENRE_IDX[g]] = 1.0

    if movie_genre_features.sum() == 0:
        return None

    return movie_genre_features

def precompute_images(resnet_encoder : ResNet50Encoder, path) -> Optional[torch.Tensor]:
    if pd.isna(path) or not path:
        return None

    if not os.path.exists(path):
        return None

    transform = transforms.Compose([
        transforms.RandomCrop((280, 280), pad_if_needed=True),
        transforms.Resize(224, interpolation=InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    img = Image.open(path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(next(resnet_encoder.parameters()).device)

    with torch.no_grad():
        poster_embed = resnet_encoder.forward(img_tensor).squeeze(0)

    return poster_embed.cpu()

def _set(features_array, mask_array, index, feature_idx, value):
    """
    Assign a value to a feature array and update the mask.
    """
    if value is not None:
        features_array[index] = value
        mask_array[index, feature_idx] = 1.0
    else:
        mask_array[index, feature_idx] = 0.0

def to_tensor_or_none(value) -> Optional[torch.Tensor]:
    if pd.isna(value):
        return None
    return torch.tensor([value], dtype=torch.float32)

if __name__ == "__main__":
    # Load mappings
    with open(os.path.join(DIR, 'mappings.pkl'), 'rb') as f:
        mappings = pickle.load(f)

    movie_db = mappings['movie_database']
    num_movies = len(movie_db)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using:", device)

    sbert = MPNetEncoder().to(device) # 768 dim
    resnet = ResNet50Encoder().to(device) # 512 dim
    word2vec = WordEmbedding() # 300 dim

    # Prepare storage (using indices)
    text_features = torch.zeros((num_movies, 768), dtype=torch.float32) # includes "TITLE: {title} TAGLINE: {tagline} OVERVIEW: {overview}"
    keywords_features = torch.zeros((num_movies, 300), dtype=torch.float32)  # make sure to split ,
    genre_features = torch.zeros((num_movies, len(ALL_GENRES)), dtype=torch.float32)  # make sure to split ,
    year_features = torch.zeros((num_movies, 1), dtype=torch.float32)
    month_sin_features = torch.zeros((num_movies, 1), dtype=torch.float32)
    month_cos_features = torch.zeros((num_movies, 1), dtype=torch.float32)
    vote_average_features = torch.zeros((num_movies, 1), dtype=torch.float32)
    vote_count_features = torch.zeros((num_movies, 1), dtype=torch.float32)
    popularity_features = torch.zeros((num_movies, 1), dtype=torch.float32)
    runtime_features = torch.zeros((num_movies, 1), dtype=torch.float32)
    poster_file_features = torch.zeros((num_movies, 512), dtype=torch.float32)
    backdrop_file_features = torch.zeros((num_movies, 512), dtype=torch.float32)

    mask_features = torch.zeros((num_movies, len(FEATURE_IDX)), dtype=torch.float32)

    for i, (tmdb_id, movie) in enumerate(tqdm(movie_db.items(), desc="Encoding movies")):
        idx = mappings['tmdb_to_idx'][tmdb_id]  # Get array index

        text_emb = get_text_features(movie, sbert)
        _set(text_features, mask_features, idx, FEATURE_IDX['text'], text_emb)

        keywords_emb = precompute_keywords(movie, word2vec)
        _set(keywords_features, mask_features, idx, FEATURE_IDX['keywords'], keywords_emb)

        genres = one_hot_encode_genres(movie)
        _set(genre_features, mask_features, idx, FEATURE_IDX['genres'], genres)

        year = to_tensor_or_none(movie.get('release_year'))
        _set(year_features, mask_features, idx, FEATURE_IDX['year'], year)

        month_sin = to_tensor_or_none(movie.get('month_sin'))
        _set(month_sin_features, mask_features, idx, FEATURE_IDX['month_sin'], month_sin)

        month_cos = to_tensor_or_none(movie.get('month_cos'))
        _set(month_cos_features, mask_features, idx, FEATURE_IDX['month_cos'], month_cos)

        vote_average = to_tensor_or_none(movie.get('vote_average'))
        _set(vote_average_features, mask_features, idx, FEATURE_IDX['vote_average'], vote_average)

        vote_count = to_tensor_or_none(movie.get('vote_count'))
        _set(vote_count_features, mask_features, idx, FEATURE_IDX['vote_count'], vote_count)

        popularity = to_tensor_or_none(movie.get('popularity'))
        _set(popularity_features, mask_features, idx, FEATURE_IDX['popularity'], popularity)

        runtime = to_tensor_or_none(movie.get('runtime'))
        _set(runtime_features, mask_features, idx, FEATURE_IDX['runtime'], runtime)

        poster_path = movie.get('poster_file')
        poster_emb = precompute_images(resnet, poster_path)
        _set(poster_file_features, mask_features, idx, FEATURE_IDX['poster'], poster_emb)

        backdrop_path = movie.get('backdrop_file')
        backdrop_emb = precompute_images(resnet, backdrop_path)
        _set(backdrop_file_features, mask_features, idx, FEATURE_IDX['backdrop'], backdrop_emb)

        if i % 100 == 0:
            torch.cuda.empty_cache()

    features = {
        "text": text_features,
        "keywords": keywords_features,
        "genres": genre_features,
        "year": year_features,
        "month_sin": month_sin_features,
        "month_cos": month_cos_features,
        "vote_average": vote_average_features,
        "vote_count": vote_count_features,
        "popularity": popularity_features,
        "runtime": runtime_features,
        "poster_file": poster_file_features,
        "backdrop_file": backdrop_file_features,
        "mask": mask_features
    }

    torch.save(features, os.path.join(DIR, "features.pt"))