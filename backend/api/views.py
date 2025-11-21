from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer, MovieSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Note
from .models import Movie


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    



class DisplayMovies(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     print("test")
    #     return Movie.objects.all().order_by('imdb_rating')[:100]

    def filter_by_genre(self, queryset, genre):
        return queryset.filter(genres__icontains=genre)
    
    def search_filter(self, queryset, searchQuery):
        return queryset.filter(title__icontains=searchQuery)

    def get_queryset(self):
        queryset = Movie.objects.all()

        genres = self.request.query_params.get("genres")
        if genres != None:
            for genre in genres.split(","):
                queryset = self.filter_by_genre(queryset, genre)

        searchQuery = self.request.query_params.get("search")
        if searchQuery != None:
            queryset = self.search_filter(queryset, searchQuery)
        
        sort_by = self.request.query_params.get("sort_by")
        if sort_by:
            print(sort_by)
            queryset = queryset.order_by(sort_by, "-popularity")
        else:
            queryset = queryset.order_by("-popularity")
        return queryset[:100]


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() #disallow create of usernames that already exist
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
