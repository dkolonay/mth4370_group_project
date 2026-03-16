[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

[contributors-shield]: https://img.shields.io/github/contributors/dkolonay/mth4370_group_project.svg?style=for-the-badge
[contributors-url]: https://github.com/dkolonay/mth4370_group_project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dkolonay/mth4370_group_project.svg?style=for-the-badge
[forks-url]: https://github.com/dkolonay/mth4370_group_project/network/members
[stars-shield]: https://img.shields.io/github/stars/dkolonay/mth4370_group_project.svg?style=for-the-badge
[stars-url]: https://github.com/dkolonay/mth4370_group_project/stargazers
[issues-shield]: https://img.shields.io/github/issues/dkolonay/mth4370_group_project.svg?style=for-the-badge
[issues-url]: https://github.com/dkolonay/mth4370_group_project/issues

<br />
<div align="center">
  <h3 align="center">Movie Recommendation System</h3>

  <p align="center">
    A full-stack movie recommendation platform powered by a multi-modal fusion model and Thompson Sampling bandit for personalization.
    <br />
    <br />
    <a href="https://github.com/dkolonay/mth4370_group_project/issues/new?labels=bug">Report Bug</a>
    ·
    <a href="https://github.com/dkolonay/mth4370_group_project/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

---

## About The Project

A movie recommendation system built as a course project for MTH 4370. The system learns rich movie embeddings from multiple modalities — text descriptions, keywords, genres, poster/backdrop images, and metadata — then uses FAISS for fast similarity search and a Thompson Sampling bandit to personalize rankings based on user interactions.

### Key Features

- **Multi-modal embeddings** — fuses text (SBERT), keywords (Word2Vec), genre vectors, image features (CNN), and scalar metadata via an attention-based fusion model trained with contrastive loss
- **Fast similarity search** — FAISS index over precomputed embeddings for sub-millisecond movie-to-movie and text query lookups
- **Personalized ranking** — Thompson Sampling bandit updates per-user alpha/beta parameters from interaction signals (clicks, likes, dislikes)
- **REST API** — Django backend exposes recommendation and user-delta endpoints with JWT auth
- **React frontend** — browseable movie feed with per-movie interaction tracking
- **Fully containerized** — Docker Compose spins up the Django app + PostgreSQL together

---

## Architecture

```
┌─────────────┐     HTTP/REST      ┌──────────────────────────────────┐
│   React UI  │ ◄────────────────► │  Django REST API (port 8000)     │
│  (Vite/JSX) │                    │  - /api/movies/                  │
└─────────────┘                    │  - /api/recommendations/         │
                                   │  - /api/user-deltas/             │
                                   └────────────┬─────────────────────┘
                                                │
                          ┌─────────────────────▼──────────────────────┐
                          │            ML Module (backend/api/ml/)      │
                          │                                             │
                          │  MovieRecommender                           │
                          │  ├── FAISS index (fused embeddings)         │
                          │  ├── FAISS index (text-only embeddings)     │
                          │  └── SBERT encoder (text queries)           │
                          │                                             │
                          │  ThomasSamplingBandit                       │
                          │  └── Re-ranks candidates using α/β params   │
                          └─────────────────────────────────────────────┘
                                                │
                                   ┌────────────▼────────────┐
                                   │    PostgreSQL (Docker)   │
                                   │  - Movies table          │
                                   │  - UserDelta table       │
                                   └─────────────────────────┘
```

---

## Recommendation System (training branch)

> The full ML pipeline lives on the [`training`](https://github.com/dkolonay/mth4370_group_project/tree/training) branch under `ml/`.

### Pipeline Overview

```
ml/
├── scripts/
│   ├── 01_dataset_downloader.sh     # Download TMDB dataset
│   ├── 02_clean_dataset.py          # Filter & clean raw data
│   ├── 03_feature_eng.py            # Engineer text, genre, metadata features
│   ├── 04_movie_node_mapping.py     # Build movie-ID → index mappings
│   ├── 04_scrape_plots_2.py         # Scrape movie plot descriptions
│   └── 05_precompute.py             # Precompute per-movie feature tensors
├── src/
│   ├── models/
│   │   └── fusion_model.py          # Multi-modal attention fusion model
│   ├── processing/
│   │   ├── sbert_encoder.py         # MPNet text encoder (768-d)
│   │   ├── keywords_encoder.py      # Word2Vec keyword encoder (300-d)
│   │   ├── cnn_encoder.py           # ResNet image encoder (512-d)
│   │   └── generate_embeddings.py   # Run all encoders → embeddings.pt
│   ├── bandits/
│   │   └── bandit.py                # Thompson Sampling bandit
│   ├── recommender system/
│   │   └── recommender.py           # FAISS-backed MovieRecommender
│   ├── contrastive_train.py         # Contrastive training loop
│   └── contrasitive_train_wplots.py # Training with loss/metric plots
└── notebooks/                       # EDA and data exploration notebooks
```

### Fusion Model

The `MovieFusionModel` projects each modality into a shared 256-d space, applies learned attention weights across modalities, then outputs a 512-d L2-normalized embedding:

| Modality | Encoder | Dim |
|---|---|---|
| Plot text | SBERT (MPNet) | 768 → 256 |
| Keywords | Word2Vec | 300 → 256 |
| Genres | One-hot (19 genres) | 19 → 256 |
| Poster image | ResNet (CNN) | 512 → 256 |
| Backdrop image | ResNet (CNN) | 512 → 256 |
| Metadata | Linear (7 scalars) | 7 → 256 |

A missing-modality mask allows the model to gracefully handle movies with incomplete data.

### Training

The model is trained with **contrastive loss** (similar movies pulled together, dissimilar pushed apart). Training scripts support checkpointing and optional loss curve plots.

### Recommender

At inference the `MovieRecommender` loads `embeddings.pt` + `mappings.pkl` into two FAISS `IndexFlatIP` (cosine similarity) indices and supports:

- **Movie → similar movies** (fused embeddings)
- **Text query → movies** (text-only embeddings + SBERT)
- **Multi-movie input** (averaged embeddings)
- **Hybrid** (movies + text combined)

### Bandit

The `ThomasSamplingBandit` maintains per-movie Beta distribution parameters (α, β) per user. Each user interaction updates the parameters via `UserDelta` records, and candidates are re-ranked by Thompson samples at request time.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, React Router, Vite |
| Backend | Django 4, Django REST Framework |
| ML | PyTorch, FAISS, sentence-transformers, scikit-learn |
| Database | PostgreSQL 14 |
| Infrastructure | Docker, Docker Compose |

---

## Getting Started

### Backend & Database (Docker)

```bash
# Clone the repository
git clone https://github.com/dkolonay/mth4370_group_project.git
cd mth4370_group_project/backend

# Start Django + PostgreSQL
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

The API will be available at `http://localhost:8000`.

### Frontend (local dev)

Requires [Node.js](https://nodejs.org/).

```bash
cd frontend

npm install
npm run dev
```

The UI will be available at `http://localhost:5173`.

### ML Training (training branch)

```bash
git checkout training
cd ml

pip install -r requirements.txt

# Run pipeline in order
bash scripts/01_dataset_downloader.sh
python scripts/02_clean_dataset.py
python scripts/03_feature_eng.py
python scripts/04_movie_node_mapping.py
python scripts/05_precompute.py

# Train the fusion model
python src/contrastive_train.py

# Generate embeddings for inference
python src/processing/generate_embeddings.py
```

---

## Table of Contents

- [About The Project](#about-the-project)
- [Architecture](#architecture)
- [Recommendation System](#recommendation-system-training-branch)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
