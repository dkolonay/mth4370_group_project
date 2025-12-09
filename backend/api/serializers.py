from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Note
from .models import Movie
from .models import UserDelta
from .models import Like

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

class UserDeltaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDelta
        fields = ["user", "movie_id", "alpha", "beta"]
        extra_kwargs = {"user" : {"read_only": True}}

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["user", "movie_id"]
        extra_kwargs = {"user": {"read_only": True}}



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
