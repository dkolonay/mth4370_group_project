from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer, MovieSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

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
    

class DisplayMovie(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"detail": "Data not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class DisplayMovies(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

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
            queryset = queryset.order_by(sort_by, "-popularity")
        else:
            queryset = queryset.order_by("-popularity")
        return queryset[:100]
    

class RecommendationsByDescription(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
   
    def get_queryset(self):
        #when model is connected, we will run the description through the model to
        #produce a list of movie ids that best fit the description

        descriptionQuery = self.request.query_params.get("description")
        # list_that_model_returns = run_description_model(descriptionQuery)
        # queryset = Movie.objects.filter(id__in=list_that_model_returns)

        print(descriptionQuery)

        queryset = Movie.objects.order_by("-popularity")[:6] #dummy response

        return queryset
    



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() #disallow create of usernames that already exist
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
