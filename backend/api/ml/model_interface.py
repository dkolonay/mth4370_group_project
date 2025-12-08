import atexit
import threading
import time
from typing import Dict, List, Union
from enum import Enum
from django.conf import settings

from .bandit import ThomasSamplingBandit
from .recommender import MovieRecommender
from .sbert_encoder import MPNetEncoder
from recommendation_system import RecommendationSystem

_REC_SYS_INSTANCE = None

class QueryType(Enum):
    TEXT = 1
    MOVIE = 2
    HYBRID = 3

def get_rec_sys_instance():
    global _REC_SYS_INSTANCE

    if _REC_SYS_INSTANCE is None:

        import pandas as pd
        df = pd.read_pickle("general_distribution.pkl")

        bandit = ThomasSamplingBandit(df)
        encoder = MPNetEncoder()
        recommender = MovieRecommender(encoder)
        _REC_SYS_INSTANCE = RecommendationSystem(recommender, bandit)

    return _REC_SYS_INSTANCE

def get_recommendations(
        qtype: QueryType,
        query: str,
        movie_ids: Union[int, List[int]],
        user_deltas: Dict[int, Dict[str, float]],
        k: int = 10
) -> List[int]:
    rec_sys = get_rec_sys_instance()

    match qtype:
        case QueryType.TEXT:
            return rec_sys.search_by_text(query, user_deltas, k)

        case QueryType.MOVIE:
            return rec_sys.search_by_movie_id(movie_ids, user_deltas, k)

        case QueryType.HYBRID:
            return rec_sys.search_by_hybrid(query, movie_ids, user_deltas, k)
