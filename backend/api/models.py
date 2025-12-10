from django.db import models
from django.contrib.auth.models import User
from typing import Dict

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes") #link user to all instances of their notes

    def __str__(self):
        return self.title
    
class Movie(models.Model):

    class Meta:
        managed=False
        db_table = 'api_movie'

    id = models.IntegerField(primary_key = True)
    title = models.CharField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    release_date = models.CharField()
    revenue = models.IntegerField()
    runtime = models.IntegerField()
    backdrop_path = models.CharField()
    budget = models.IntegerField()
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField()
    tagline = models.TextField()
    genres = models.CharField()
    keywords = models.CharField()

    def __str__(self):
        return self.title
    
class UserDeltas(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="deltas")
    deltas = models.JSONField(default=dict)

    @property
    def deltas_int_keys(self) -> Dict[int, Dict[str, float]]:
        return {int(k): v for k, v in self.deltas.items()}

    def update_from_bandit(self, movie_id, bandit_result):
        movie_id = str(movie_id)
        if movie_id not in self.deltas:
            self.deltas[movie_id] = {"alpha": 0.0, "beta": 0.0}

        self.deltas[movie_id]["alpha"] = bandit_result["new_alpha_delta"]
        self.deltas[movie_id]["beta"] = bandit_result["new_beta_delta"]
        self.save()
        return self.deltas
    
    def get_deltas(self, movie_id: int) -> Dict[str, float]:
        return self.deltas_int_keys.get(movie_id, {"alpha": 0.0, "beta": 0.0})
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="likes")
    
    class Meta:
        unique_together = (('user', 'movie_id'),)

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dislikes")
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="dislikes")
    
    class Meta:
        unique_together = (('user', 'movie_id'),)

