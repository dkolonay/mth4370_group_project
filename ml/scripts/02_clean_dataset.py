"""
Organizes the cleaning process from the Jupyter notebook
"""

import pandas as pd
import os
import re

def remove_duplicates(cols, df):
    # ranking
    df_sorted = df.sort_values(by=['vote_count', 'popularity'], ascending=False)

    # Drop duplicates based on title + release_date, keeping highest ranked
    df_deduped = df_sorted.drop_duplicates(subset=cols, keep='first')

    return df_deduped.reset_index(drop=True)

if __name__ == "__main__":
    # Load data
    path = os.path.join(os.getcwd(), '..', 'data', 'raw', 'TMDB_movie_dataset_v11.csv')
    df = pd.read_csv(path)

    # Define columns to ignore
    pre_ignore_cols = [
        'production_companies',
        'production_countries',
        'original_language',
        'homepage',
        'imdb_id',
        'status',
        'original_title'
    ]

    post_ignore_cols = [
        'spoken_languages',
        'adult'
    ]

    print('cleaning dataset...')
    print('pre-filtering...')
    # Drop pre-filter columns
    pre_filtered_df = df.drop(columns=pre_ignore_cols)

    print('removing null titles')
    # Remove titles that are null
    pre_filtered_df = pre_filtered_df.dropna(subset=['title'])

    # deduping based off
    cols = ['title', 'release_date']

    cols2 = ['id', 'title']

    cols3 = ['id', 'poster_path']

    cols4 = ['title', 'poster_path']

    cols5 = ['title', 'backdrop_path']

    print('removing duplicate title x realease_date')
    pre_filtered_df = remove_duplicates(cols, pre_filtered_df)

    print('removing duplicate id x title')
    pre_filtered_df = remove_duplicates(cols2, pre_filtered_df)

    print('removing duplicate id x poster_path')
    pre_filtered_df = remove_duplicates(cols3, pre_filtered_df)

    print('removing duplicate title x poster_path')
    pre_filtered_df = remove_duplicates(cols4, pre_filtered_df)

    print('removing duplicate id x backdrop_path')
    pre_filtered_df = remove_duplicates(cols5, pre_filtered_df)

    print('post-filtering...')
    # filtering to keep only English and non adult movies
    df_filtered_lang = pre_filtered_df[pre_filtered_df['spoken_languages'].str.contains('English', na=False)]
    df_filtered_adult = df_filtered_lang[df_filtered_lang['adult'] == False]
    post_filtered_df = df_filtered_adult.drop(columns=post_ignore_cols)

    print('keeping titles with at least one english char')
    mask = post_filtered_df['title'].str.contains(r'[A-Za-z]', regex=True)

    post_filtered_df = post_filtered_df[mask].copy()

    # Number of duplicate values per column
    duplicates_per_col = post_filtered_df.apply(lambda col: col.duplicated().sum())
    print(duplicates_per_col)

    print('saving cleaned dataset...')
    output_path = os.path.abspath('../data/processed')
    post_filtered_df.to_csv(output_path + '/movie_dataset_cleaned.csv', index=False)