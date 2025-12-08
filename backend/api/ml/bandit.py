from typing import List, Dict, Any

import pandas as pd
import torch
from abc import ABC, abstractmethod
from enum import Enum

class ActionType(Enum): #values to be decided
    # alpha, beta
    IGNORE = (0.0, 0.0)
    CLICK = (0.0, 0.0)
    LIKED = (0.0, 0.0)
    DISLIKED = (0.0, 0.0)

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

        self.df = global_df.set_index('id')
        self.df['alpha'] = self.df['alpha'].astype(float)
        self.df['beta'] = self.df['beta'].astype(float)

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

        subset = self.df.loc[candidate_ids]

        batch_alpha = torch.tensor(subset['alpha'].values, dtype=torch.float32)
        batch_beta = torch.tensor(subset['beta'].values, dtype=torch.float32)

        # 3. Apply User Context (The "Filling" of the sandwich)
        # We add the user's stored Deltas to the Global Alphas
        if user_deltas:
            id_to_idx = {movie_id: i for i, movie_id in enumerate(candidate_ids)}
            for movie_id, stats in user_deltas.items():
                if movie_id in id_to_idx:
                    idx = id_to_idx[movie_id]
                    batch_alpha[idx] += stats.get('alpha', 0.0)
                    batch_beta[idx] += stats.get('beta', 0.0)

        # 4. Thompson Sampling
        sampled_scores = torch.distributions.Beta(batch_alpha, batch_beta).sample()

        # 5. Top K Selection
        _, indices = torch.topk(sampled_scores, k=k)

        return [candidate_ids[i] for i in indices.numpy()]

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

        g_alpha = alpha_inc
        g_beta = beta_inc

        self.df.at[movie_id, 'alpha'] += g_alpha
        self.df.at[movie_id, 'beta'] += g_beta

        # Return Transaction
        current_stats = user_deltas.get(movie_id, {'alpha': 0.0, 'beta': 0.0})

        return {
            'movie_id': movie_id,
            'global_update': {'alpha_inc': g_alpha, 'beta_inc': g_beta}, # returns increments
            'user_update': {
                'new_alpha_delta': current_stats['alpha'] + p_alpha, # returns total
                'new_beta_delta': current_stats['beta'] + p_beta
            }
        }