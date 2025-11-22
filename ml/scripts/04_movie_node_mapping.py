"""
  Create sequential node indices from movie IDs for GNNs.
"""

import pandas as pd
import pickle
import os

if __name__ == '__main__':
    df = pd.read_csv(os.path.abspath("../data/processed/movie_dataset_processed.csv"))

    # Convert dataframe to list of dicts for consistency
    movies = df.to_dict(orient='records')

    # Sort by movie ID for consistent indexing
    movies = sorted(movies, key=lambda x: x['id'])

    # Create mappings
    movie_id_to_idx = {}
    idx_to_movie_id = {}
    movie_database = {}

    for idx, movie in enumerate(movies):
        movie_id = movie['id']
        movie_id_to_idx[movie_id] = idx
        idx_to_movie_id[idx] = movie_id
        movie_database[movie_id] = movie

    # Prepare final mappings dict
    mappings = {
        'tmdb_to_idx': movie_id_to_idx,
        'idx_to_tmdb': idx_to_movie_id,
        'movie_database': movie_database
    }

    # Ensure processed folder exists
    save_path = os.path.abspath("../data/processed/mappings.pkl")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save mappings as pickle
    with open(save_path, "wb") as f:
        pickle.dump(mappings, f)

    print(f"Created mappings for {len(movies)} movies")
    print(f"Index range: 0 to {len(movies)-1}")