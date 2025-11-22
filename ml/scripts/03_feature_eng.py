'''
id
title (ord) (encode) - title of movie


eng_from:
vote_average (ord) to (normalize)- average rating of movie
vote_count (ord) (log) to (normalize)- number of votes of movie
runtime (ord) to (yj) to (normalize)
release_date // parse year (ord) to (normalize)
popularity (ord) to (log) to (normalize)


back_drop_path (ord) (get image form link) (encode)
overview (ord) (encode)
poster_path (ord) (encode)
tagline (ord) (encode)
genres (cat) (one hot encoded)
keywords (multi-hot encoded) or (use pretrained word2vec then pool)
'''

#T

import pandas as pd
import numpy as np

from sklearn.preprocessing import PowerTransformer, StandardScaler

import os
import asyncio
import aiohttp

from PIL import Image
from io import BytesIO

CONCURRENCY = 20   # try 20–50;

def make_url(path, size="w185"):
    if not isinstance(path, str) or path.strip() == "":
        return None
    return f"https://image.tmdb.org/t/p/{size}/{path}"

async def fetch_image(session, url):
    if url is None:
        return None

    for attempt in range(5):
        try:
            async with session.get(url) as resp:

                if resp.status == 429:
                    retry_after = resp.headers.get("Retry-After")
                    wait = int(retry_after) if retry_after else 2
                    await asyncio.sleep(wait)
                    continue

                if resp.status != 200:
                    return None

                return await resp.read()

        except:
            await asyncio.sleep(0.5 * (2 ** attempt))  # backoff

    print(f"[ERROR] Failed to fetch image: {url}")
    return None

async def download_one(semaphore, session, url, save_path):
    async with semaphore:
        # Skip if already downloaded
        if os.path.exists(save_path):
            return save_path

        if url is None:
            return None

        data = await fetch_image(session, url)
        if data is None:
            return None

        try:
            img = Image.open(BytesIO(data)).convert("RGB")
            img.save(save_path)
            return save_path
        except Exception:
            return None


async def download_all_async(df):
    semaphore = asyncio.Semaphore(CONCURRENCY)
    async with aiohttp.ClientSession() as session:

        poster_tasks = []
        backdrop_tasks = []

        for idx, row in df.iterrows():
            poster_url = row["poster_url"]
            poster_save = os.path.abspath(f"../data/images/posters/{idx}.jpg")

            backdrop_url = row["backdrop_url"]
            backdrop_save = os.path.abspath(f"../data/images/backdrops/{idx}.jpg")

            poster_tasks.append(
                download_one(semaphore, session, poster_url, poster_save)
            )
            backdrop_tasks.append(
                download_one(semaphore, session, backdrop_url, backdrop_save)
            )

        poster_paths = await asyncio.gather(*poster_tasks)
        backdrop_paths = await asyncio.gather(*backdrop_tasks)

        return poster_paths, backdrop_paths

if __name__ == '__main__':
    df = pd.read_csv(os.path.abspath("../data/processed/movie_dataset_cleaned.csv"))

    print('[1] removing revenue and budget columns')
    df.drop(['revenue', 'budget'], axis=1, inplace=True)

    print('[2] generating poster/backdrop URLs')
    df["poster_url"] = df["poster_path"].apply(make_url)
    df["backdrop_url"] = df["backdrop_path"].apply(make_url)

    print('[3] creating image folders...')
    base_img_path = os.path.abspath("../data/images")
    poster_dir = os.path.join(base_img_path, "posters")
    backdrop_dir = os.path.join(base_img_path, "backdrops")

    os.makedirs(poster_dir, exist_ok=True)
    os.makedirs(backdrop_dir, exist_ok=True)

    print('[4] downloading images async...')

    poster_paths, backdrop_paths = asyncio.run(download_all_async(df))

    df["poster_file"] = poster_paths
    df["backdrop_file"] = backdrop_paths

    print('[5] dropping unused URL/path columns...')
    df = df.drop(columns=["poster_path", "backdrop_path", "poster_url", "backdrop_url"])

    print('[6] extracting year + month_sin/cos features...')
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    df['release_year'] = df['release_date'].dt.year # scale

    month = df['release_date'].dt.month
    df['month_sin'] = np.sin(2 * np.pi * month / 12) # scale
    df['month_cos'] = np.cos(2 * np.pi * month / 12) # scale

    df.drop(['release_date'], axis=1, inplace=True)

    print('[7] applying log + yeo-johnson transforms...')
    log_features = ['vote_count', 'popularity']
    yj_features = ['runtime']

    for feat in log_features:
        df[feat] = np.log1p(df[feat])

    for feat in yj_features:
        yj = PowerTransformer(method="yeo-johnson")
        df[feat] = yj.fit_transform(df[[feat]])

    print('[8] applying StandardScaler...')
    scaler = StandardScaler()
    scale_features = yj_features + log_features + ['month_sin', 'month_cos', 'release_year', 'vote_average']

    df[scale_features] = scaler.fit_transform(df[scale_features])

    print('[9] saving final processed CSV...')
    df.to_csv(os.path.abspath("../data/processed/movie_dataset_processed.csv"), index=False)