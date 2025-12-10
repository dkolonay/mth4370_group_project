from django.db import models
from django.contrib.auth.models import User

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
    
class UserDelta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_deltas")
    movie_id = models.IntegerField()
    alpha = models.FloatField()
    beta = models.FloatField()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="likes")
    
    class Meta:
        unique_together = (('user', 'movie_id'),)

