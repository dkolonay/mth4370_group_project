import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DIR = os.path.join(PROJECT_ROOT, "data", "processed")


def get_id_to_score_map(dataset_path):
    # 1. Read and Sort
    df = pd.read_csv(dataset_path)
    df = df.sort_values(by='id').reset_index(drop=True)

    # 2. Calculate Weighted Score
    C = df['vote_average'].mean()
    m = df['vote_count'].quantile(0.50)
    v = df['vote_count'].fillna(0)
    R = df['vote_average'].fillna(C)

    # Store temporary weighted score in DF
    df['weighted_score'] = (v / (v + m) * R) + (m / (v + m) * C)

    # 3. Calculate Priors
    df['prior_mean'] = np.clip(df['weighted_score'] / 10.0, 0.05, 0.95)

    # 20 because 100, would make this as base truth,
    # but I want to use it as a warm start.
    df['alpha'] = df['prior_mean'] * 20
    df['beta'] = (1 - df['prior_mean']) * 20

    return df


if __name__ == '__main__':
    # Get the map and the dataframe
    df = get_id_to_score_map(os.path.join(DIR, 'movie_dataset_cleaned.csv'))

    df[['id', 'alpha', 'beta']].to_csv('../data/processed/movie_prob.csv', index=False)