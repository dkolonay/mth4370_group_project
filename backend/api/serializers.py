from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Note
from .models import Movie

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}} #password not returned when reading info about user

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}} #author name can be read but not changed

# class MovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = ["_id", "genres", "image_url", "imdb_id", "imdb_link", "movie_id", "movie_title", "original_language", "overview", "popularity", "production_countries", "release_date", "runtime", "spoken_languages", "tmdb_id", "tmdb_link", "vote_average", "vote_count", "year_released"]

#         def save(self, *args, **kwargs):
#             return
        
#         def delete(self, *args, **kwargs):
#             return
        
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["poster_link", "title", "release_year", "certif", "runtime", "genres", "imdb_rating", "overview", "meta_score", "director", "star_one", "star_two", "star_three", "star_four", "num_votes", "gross"]
