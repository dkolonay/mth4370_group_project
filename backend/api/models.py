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
    

# class Movie(models.Model):
#     _id = models.CharField(max_length = 255)
#     genres = ArrayField(
#         models.CharField(max_length = 255),
#         blank=True,
#         null=True
#     )
#     image_url = models.CharField(max_length = 255, blank=True, null=True)
#     imdb_id = models.CharField(max_length = 255, blank=True, null=True)
#     imdb_link = models.URLField(max_length = 2048, blank=True, null=True)
#     movie_id = models.CharField(max_length = 255)
#     movie_title = models.CharField(max_length = 255)
#     original_language = models.CharField(max_length = 255, blank=True, null=True)
#     overview = models.TextField()
#     popularity = models.FloatField(blank=True, null=True)
#     production_countries = ArrayField(
#         models.CharField(max_length = 255),
#         blank = True,
#         null = True
#     )
#     release_data = models.CharField(max_length= 255, blank=True, null= True)
#     runtime = models.CharField(max_length = 255, blank=True, null=True)
#     spoken_languages = ArrayField(
#         models.CharField(max_length = 255),
#         blank = True,
#         null = True
#     )
#     tmdb_id = models.CharField(max_length=255, blank=True, null=True) #might be of a problematic type
#     tmdb_link = models.URLField(max_length = 2048, blank= True, null = True)
#     vote_average = models.CharField(max_length= 255, blank=True, null= True)
#     vote_count = models.CharField(max_length= 255, blank=True, null= True)
#     year_released = models.CharField(max_length= 255, blank=True, null= True)

#     def __str__(self):
#         return self.movie_title
    

class Movie(models.Model):

    class Meta:
        managed=False
        db_table = 'api_movie'


    title = models.CharField(max_length = 255,primary_key=True)
    poster_link = models.CharField(max_length = 255, blank=True, null=True)
    release_year = models.CharField(max_length = 255, blank=True, null=True)
    certif = models.CharField(max_length = 255, blank=True, null=True)
    runtime = models.CharField(max_length = 255, blank=True, null=True)
    genres = models.CharField(max_length = 255, blank=True, null=True)
    imdb_rating = models.CharField(max_length = 255, blank=True, null=True)
    overview = models.CharField(max_length = 255, blank=True, null=True)
    meta_score = models.CharField(max_length = 255, blank=True, null=True)
    director = models.CharField(max_length = 255, blank=True, null=True)
    star_one = models.CharField(max_length = 255, blank=True, null=True)
    star_two = models.CharField(max_length = 255, blank=True, null=True)
    star_three = models.CharField(max_length = 255, blank=True, null=True)
    star_four = models.CharField(max_length = 255, blank=True, null=True)
    num_votes = models.CharField(max_length = 255, blank=True, null=True)
    gross = models.CharField(max_length = 255, blank=True, null=True)
    

    def __str__(self):
        return self.title