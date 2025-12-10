from typing import List, Dict, Any

import pandas as pd
import torch
from abc import ABC, abstractmethod
from enum import Enum

class ActionType(Enum): #values to be decided
    # alpha, beta
    IGNORE = (0.0, 0.0)
    CLICK = (1.0, 0.0)
    LIKED = (2.0, 0.0)
    DISLIKED = (0.0, 3.0)

class Bandit(ABC):
    @abstractmethod
    def rank(self, user_deltas, candidate_ids, k=10):
        return None

    @abstractmethod
    def calculate_interaction(self, user_deltas, movie_id, action_type: ActionType):
        return None

class ThomasSamplingBandit(Bandit):
    def __init__(self, global_df: pd.DataFrame, personal_lr=2):
        """
        global_df: DataFrame with ['id', 'alpha', 'beta']
        personal_lr: Learning rate for the user
        """
        self.personal_lr = personal_lr

        self.df = global_df
        self.stats = self.df.set_index('id')[['alpha', 'beta']].to_dict('index')

    def rank(
            self,
            user_deltas: Dict[int, Dict[str, float]],
            candidate_ids: List,
            k=10
    ) -> List[int]:
        """
        Ranks movies by combining Global Wisdom + User Context.

        user_deltas: Dict { movie_id: {'alpha': 2.0, 'beta': 0.0} }
        candidate_ids: List of IDs
        """
        if len(candidate_ids) < k:
            raise "length of candidate_ids should be greater than or equal to k"

        ranked_candidates = []

        for movie_id in candidate_ids:
            alpha = self.stats[movie_id]['alpha']
            beta = self.stats[movie_id]['beta']

            if movie_id in user_deltas:
                alpha += user_deltas[movie_id].get('alpha', 0.0)
                beta += user_deltas[movie_id].get('beta', 0.0)

            ranked_candidates.append({
                'id': movie_id,
                'score': torch.distributions.Beta(float(alpha), float(beta)).sample()
            })


        ranked_candidates.sort(key=lambda x: x['score'], reverse=True)

        return [item['id'] for item in ranked_candidates[:k]]

    def calculate_interaction(
            self,
            user_deltas: Dict[int, Dict[str, float]],
            movie_id: int,
            action_type: ActionType
    ) -> Dict[str, Any]:
        """
        Calculates updates. Assumes movie_id is valid.
        """
        alpha_inc, beta_inc = action_type.value

        # Calculate Updates
        p_alpha = alpha_inc * self.personal_lr
        p_beta = beta_inc * self.personal_lr

        self.stats[movie_id]['alpha'] += alpha_inc
        self.stats[movie_id]['beta'] += beta_inc

        # Return Transaction
        current_stats = user_deltas.get(movie_id, {'alpha': 0.0, 'beta': 0.0})

        return {
            'movie_id': movie_id,
            'global_update': {'alpha_inc': alpha_inc, 'beta_inc': beta_inc}, # returns increments
            'user_update': {
                'new_alpha_delta': current_stats['alpha'] + p_alpha, # returns total
                'new_beta_delta': current_stats['beta'] + p_beta
            }
        }