from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

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
    # _status = models.CharField()
    release_date = models.CharField()
    revenue = models.IntegerField()
    runtime = models.IntegerField()
    # adult = models.BooleanField()
    backdrop_path = models.CharField()
    budget = models.IntegerField()
    # homepage = models.URLField()
    # imdb_id = models.CharField()
    # original_language = models.CharField()
    # original_title = models.CharField()
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField()
    tagline = models.TextField()
    genres = models.CharField()
    # production_companies = models.CharField()
    # production_countries = models.CharField()
    # spoken_languages = models.CharField()
    keywords = models.CharField()

    def __str__(self):
        return self.title
