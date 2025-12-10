from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Movie
from .models import UserDeltas
from .models import Like
from .models import Dislike

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}} #password not returned when reading info about user

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class MovieSerializer(serializers.ModelSerializer):
    liked = serializers.BooleanField(read_only=True)     # <- include annotation
    disliked = serializers.BooleanField(read_only=True) 

    class Meta:
        model = Movie
        fields = ["id", "title", "vote_count", "vote_average", "release_date", "runtime", "backdrop_path", "overview", "poster_path", "tagline", "genres", "liked", "disliked"  ]
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["user", "movie_id"]
        extra_kwargs = {"user": {"read_only": True}}

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ["user", "movie_id"]
        extra_kwargs = {"user": {"read_only": True}}

class UserDeltasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDeltas
        fields = ['user', 'deltas']

    def create(self, validated_data):
        return UserDeltas.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.deltas = validated_data.get('deltas', instance.deltas)
        instance.save()
        return instance


