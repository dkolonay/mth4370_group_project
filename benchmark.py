"""
Benchmark script for the FAISS recommendation inference speed.
Run from the root of the project:

    python benchmark.py

Delete this file when done.
"""

import time
import pickle
import random
import statistics

import torch
import torch.nn.functional as F
import faiss

# ── paths (relative to project root) ────────────────────────────────────────
EMBEDDINGS_PATH = "backend/api/ml/data/embeddings_wp.pt"
MAPPINGS_PATH   = "backend/api/ml/data/mappings_no_dataset.pkl"
N_RUNS          = 200   # number of queries to average over
K               = 10    # recommendations per query

# ── load data ────────────────────────────────────────────────────────────────
print("Loading embeddings and mappings...")
t0 = time.perf_counter()

embeddings_dict   = torch.load(EMBEDDINGS_PATH, weights_only=False)
fused_embeddings  = embeddings_dict["fused"]
num_movies, embed_dim = fused_embeddings.shape

with open(MAPPINGS_PATH, "rb") as f:
    mappings = pickle.load(f)

tmdb_ids = list(mappings["tmdb_to_idx"].keys())
tmdb_to_idx = mappings["tmdb_to_idx"]

load_time = time.perf_counter() - t0
print(f"  {num_movies:,} movies  |  {embed_dim}-d embeddings  |  loaded in {load_time:.2f}s\n")

# ── build FAISS index ────────────────────────────────────────────────────────
print("Building FAISS index...")
t0 = time.perf_counter()

emb_np = fused_embeddings.cpu().numpy().astype("float32")
faiss.normalize_L2(emb_np)
index = faiss.IndexFlatIP(embed_dim)
index.add(emb_np)

index_time = time.perf_counter() - t0
print(f"  Index built in {index_time:.3f}s\n")

# ── benchmark: movie-to-movie queries ────────────────────────────────────────
print(f"Running {N_RUNS} movie-to-movie queries (k={K})...")

latencies_ms = []
sample_ids = random.choices(tmdb_ids, k=N_RUNS)

for tmdb_id in sample_ids:
    idx = tmdb_to_idx[tmdb_id]
    query = fused_embeddings[[idx]]
    query = F.normalize(query, p=2, dim=1)
    query_np = query.cpu().numpy().astype("float32")

    t0 = time.perf_counter()
    index.search(query_np, K + 1)   # +1 to allow excluding self
    latencies_ms.append((time.perf_counter() - t0) * 1000)

mean_ms   = statistics.mean(latencies_ms)
median_ms = statistics.median(latencies_ms)
p99_ms    = sorted(latencies_ms)[int(0.99 * N_RUNS)]
min_ms    = min(latencies_ms)
max_ms    = max(latencies_ms)

print(f"\n{'─'*40}")
print(f"  Movie-to-movie FAISS search ({N_RUNS} runs, k={K})")
print(f"{'─'*40}")
print(f"  Mean:    {mean_ms:.3f} ms")
print(f"  Median:  {median_ms:.3f} ms")
print(f"  p99:     {p99_ms:.3f} ms")
print(f"  Min:     {min_ms:.3f} ms")
print(f"  Max:     {max_ms:.3f} ms")
print(f"{'─'*40}")
print(f"\nDataset size: {num_movies:,} movies")
print("\nUse the MEAN or MEDIAN in your resume bullet.")
