from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer, MovieSerializer, UserDeltaSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Movie, UserDelta, Like

from .ml.model_interface import get_recommendations, QueryType
#I want to initialize _REC_INSTANCE on startup

class UserDeltaListCreate(generics.ListCreateAPIView):
    serializer_class = UserDeltaSerializer
    permission_classes = [IsAuthenticated]
    

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user = self.request.user)
        else:
            print(serializer.errors)

    def get_queryset(self):
        user = self.request.user
        return UserDelta.objects.filter(user=user)
    
class LikeListCreate(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request)
        serializer.save(user = self.request.user)
     

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)
    

class DisplayMovie(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            is_liked = Like.objects.filter(user=request.user, movie_id=pk).exists()
            serializer = MovieSerializer(movie)
          
            return Response({'movie_data': serializer.data, 'liked': is_liked}, status=status.HTTP_200_OK)
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
        description_query = self.request.query_params.get("description")
        recommended_ids = get_recommendations(qtype = QueryType.TEXT, query= description_query, k= 100)
        queryset = Movie.objects.filter(id__in = recommended_ids)
        queryset = queryset.filter(vote_count__gt=10) #Some strange movies show up when 0 votes are allowed

        return queryset
    
class RecommendationsByMovieIds(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        movie_ids_query = self.request.query_params.get("movie_ids")
        query_ids = [int(id_string) for id_string in movie_ids_query.split(",")]

        recommended_ids = get_recommendations(qtype = QueryType.MOVIE, movie_ids = query_ids, k= 100)
        queryset = Movie.objects.filter(id__in = recommended_ids)
        queryset = queryset.filter(vote_count__gt=10) #Some strange movies show up when 0 votes are allowed

        return queryset
    
class RecommendationsHybrid(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        movie_ids_query_string = self.request.query_params.get("movie_ids")
        query_ids = [int(id_string) for id_string in movie_ids_query_string.split(",")]

        description_query = self.request.query_params.get("description")

        recommended_ids = get_recommendations(qtype = QueryType.HYBRID, query=description_query, movie_ids=query_ids, k=100)

        queryset = Movie.objects.filter(id__in = recommended_ids)
        queryset = queryset.filter(vote_count__gt=10) #Some strange movies show up when 0 votes are allowed

        return queryset


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() #disallow create of usernames that already exist
    serializer_class = UserSerializer
    permission_classes = [AllowAny]




# class NoteListCreate(generics.ListCreateAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Note.objects.filter(author=user)
    
#     def perform_create(self, serializer):
#         if serializer.is_valid():
#             serializer.save(author=self.request.user)
#         else:
#             print(serializer.errors)

# class NoteDelete(generics.DestroyAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Note.objects.filter(author=user)
