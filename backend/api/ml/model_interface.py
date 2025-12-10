import os
from typing import Dict, List, Union
from enum import Enum
from django.conf import settings
import pandas as pd

from .bandit import ThomasSamplingBandit, ActionType
from .recommender import MovieRecommender
from .sbert_encoder import MPNetEncoder
from .recommendation_system import RecommendationSystem

ml_path = settings.ML_PATH

_REC_SYS_INSTANCE = None

if _REC_SYS_INSTANCE is None:
    df = pd.read_pickle(os.path.join(ml_path, "data", "general_distribution.pkl"))

    bandit = ThomasSamplingBandit(df)
    encoder = MPNetEncoder()
    recommender = MovieRecommender(encoder)

    _REC_SYS_INSTANCE = RecommendationSystem(recommender, bandit)

class QueryType(Enum):
    TEXT = 1
    MOVIE = 2
    HYBRID = 3



def get_recommendations(
        qtype: QueryType,
        query: str = None,
        movie_ids: Union[int, List[int]] = None,
        user_deltas: Dict[int, Dict[str, float]] = None,
        k: int = 10
) -> List[int]:
    rec_sys = _REC_SYS_INSTANCE

    match qtype:
        case QueryType.TEXT:
            return rec_sys.search_by_text(query, user_deltas, k)

        case QueryType.MOVIE:
            return rec_sys.search_by_movie_id(movie_ids, user_deltas, k)

        case QueryType.HYBRID:
            return rec_sys.search_by_hybrid(query, movie_ids, user_deltas, k)
        

def bandit_interraction(
            user_deltas: Dict[int, Dict[str, float]],
            movie_id: int,
            action_type: ActionType
    ) -> Dict[str, float]:

    updated_deltas = bandit.calculate_interaction(user_deltas, movie_id, action_type)
    return updated_deltas['user_update']

