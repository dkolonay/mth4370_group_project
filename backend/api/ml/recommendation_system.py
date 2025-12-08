from typing import Dict, List, Union

from .bandit import Bandit
from .recommender import MovieRecommender

class RecommendationSystem:
    def __init__(self, recommender: MovieRecommender, bandit: Bandit ):
        self.recommender = recommender
        self.bandit = bandit


    def personalized(self, candidate_ids: List, user_deltas: Dict[int, Dict[str, float]] = {}, k=10) -> List[int]: 
            return self.bandit.rank(user_deltas, candidate_ids, k)
    
    def search_by_text(self, query, user_deltas: Dict[int, Dict[str, float]] = {}, k=10):
         candidate_ids = self.recommender.search_by_text(query, 1000)
         return self.personalized(candidate_ids, user_deltas, k)
    
    def search_by_movie_id(self, movie_ids: Union[int, List[int]], user_deltas: Dict[int, Dict[str, float]] = {}, k=10):
        candidate_ids = self.recommender.search_by_movie_ids(movie_ids, 1000)
        return self.personalized(candidate_ids, user_deltas, k)
    
    def search_hybrid(self, query, movie_ids: Union[int, List[int]], user_deltas: Dict[int, Dict[str, float]] = {}, k=10):
        candidate_ids = self.recommender.search_hybrid(movie_ids, query, 0.5, 1000)
        return self.personalized(candidate_ids, user_deltas, k)
         
        
