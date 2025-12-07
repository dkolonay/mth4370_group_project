import random
import pickle
import os
import asyncio
import time
from typing import List, Optional, Tuple
import concurrent.futures

import requests
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DIR = os.path.join(PROJECT_ROOT, "data", "processed")

WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
TMDB_PROPERTY = "P4947"

DROPOUT = 0.20
SEED = 42

HEADERS = {
    "User-Agent": "MTH4370_Group_Project_Bot/1.0 (student_project_scraping)"
}

def extract_plot(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, 'html.parser')

    header = soup.find(id="Plot")
    if not header:
        return None

    def is_heading_wrapper(tag):
        return tag.name == 'div' and tag.has_attr('class') and any(
            c in tag.get('class') for c in ['mw-heading', 'section-heading'])

    wrapper = header.find_parent(is_heading_wrapper)
    start_node = wrapper if wrapper else header

    extracted_paragraphs = []

    for sibling in start_node.next_siblings:
        if not sibling.name:
            continue
        if sibling.name == 'h2':
            break
        if is_heading_wrapper(sibling):
            if sibling.find('h2'):
                break
        if sibling.name == 'p':
            extracted_paragraphs.append(sibling.get_text().strip())
        if sibling.name == 'section':
            for p in sibling.find_all('p'):
                extracted_paragraphs.append(p.get_text().strip())
    return " ".join(extracted_paragraphs)


def fetch_plot(movie_id: int, wiki_link: str) -> Tuple[int, Optional[str]]:
    try:
        # Use a random user agent for every request to avoid blocking
        response = requests.get(wiki_link, headers=HEADERS, timeout=10)

        if response.status_code == 404:
            return movie_id, None

        response.raise_for_status()

        # Pass the text to your extractor
        plot = extract_plot(response.text)
        return movie_id, plot

    except Exception as e:
        print(f"  -> Error: {e}")
        return movie_id, None


def fetch_wiki_url(movie_id: int) -> Tuple[int, Optional[str]]:
    sparql_query = f"""
    SELECT ?enwiki_url
    WHERE {{
      ?item wdt:{TMDB_PROPERTY} "{movie_id}" .
      ?enwiki_url schema:about ?item .
      ?enwiki_url schema:inLanguage "en" .
      ?enwiki_url schema:isPartOf <https://en.wikipedia.org/> .
    }}
    """

    url = WIKIDATA_SPARQL_ENDPOINT
    params = {'query': sparql_query, 'format': 'json'}

    max_retries = 5
    base_delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=10)
            if response.status_code == 429:
                sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                time.sleep(sleep_time)
                continue

            if response.status_code != 200:
                return movie_id, None

            data = response.json()
            bindings = data.get('results', {}).get('bindings', [])

            if bindings:
                wiki_url = bindings[0].get('enwiki_url', {}).get('value')
                return movie_id, wiki_url

            return movie_id, None

        except Exception as e:
            print(f"Error encountered: {e}")
            return movie_id, None


def fetch_wiki_urls(movie_ids: List[int]) -> List[Tuple[int, Optional[str]]]:
    values_str = " ".join([f'"{mid}"' for mid in movie_ids])

    sparql_query = f"""
    SELECT ?tmdb_id ?enwiki_url
    WHERE {{
      VALUES ?tmdb_id {{ {values_str} }}
      ?item wdt:{TMDB_PROPERTY} ?tmdb_id .
      ?enwiki_url schema:about ?item .
      ?enwiki_url schema:inLanguage "en" .
      ?enwiki_url schema:isPartOf <https://en.wikipedia.org/> .
    }}
    """

    url = WIKIDATA_SPARQL_ENDPOINT
    params = {'query': sparql_query, 'format': 'json'}

    results_map = {movie_id: None for movie_id in movie_ids}

    for attempt in range(5):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=15)

            if response.status_code == 429:
                time.sleep(2 * (2**attempt)) # Exponential backoff
                continue

            if response.status_code != 200:
                return [(mid, None) for mid in movie_ids]

            data = response.json()
            bindings = data.get('results', {}).get('bindings', [])

            for b in bindings:
                found_id = int(b['tmdb_id']['value'])
                found_url = b['enwiki_url']['value']
                results_map[found_id] = found_url

            return list(results_map.items())

        except Exception:
            return [(mid, None) for mid in movie_ids]

    return [(mid, None) for mid in movie_ids]

async def process(movie_ids: List[int]) -> List[Tuple[int, Optional[str]]]:
    loop = asyncio.get_event_loop()

    # 1. SPLIT INTO BATCHES OF 50
    BATCH_SIZE = 50
    batches = [movie_ids[i:i + BATCH_SIZE] for i in range(0, len(movie_ids), BATCH_SIZE)]

    print(f"Fetching urls")
    url_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    url_tasks = []
    for batch in batches:
            task = loop.run_in_executor(url_executor, fetch_wiki_urls, batch)
            url_tasks.append(task)

    batch_results = await tqdm.gather(*url_tasks, desc="Scraping Wikidata")

    # Flatten results (list of lists -> list of tuples)
    flat_results = [item for sublist in batch_results for item in sublist]

    url_executor.shutdown()

    print(f"Fetching Plots")
    plot_executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    plot_tasks = []

    for movie_id, url in flat_results:
        if url:
            task = loop.run_in_executor(plot_executor, fetch_plot, movie_id, url)
            plot_tasks.append(task)
        else:
            plot_tasks.append(asyncio.sleep(0, result=(movie_id, None)))

    final_results = await tqdm.gather(*plot_tasks, desc="Scraping Plots")
    plot_executor.shutdown()

    return final_results

async def main(movie_ids: List[int]) -> list[tuple[int, str | None]]:
    return await process(movie_ids)

if __name__ == "__main__":
    random.seed(SEED)
    with open(os.path.join(DIR, "mappings.pkl"), "rb") as f:
        mappings = pickle.load(f)

    movie_database = mappings['movie_database']
    movie_ids_to_scrape = list(movie_database.keys())

    results = asyncio.run(main(movie_ids_to_scrape))

    for movie_id, plot in results:
        if plot:
            movie_database[movie_id]['plot'] = plot

    save_path = os.path.join(DIR, "mappings_with_plots.pkl")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        pickle.dump(mappings, f)