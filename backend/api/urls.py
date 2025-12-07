from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("movies/", views.DisplayMovies.as_view(), name="movie-list"),
    path("movie/<int:pk>/", views.DisplayMovie.as_view(), name="movie"),
    path("recommendations/by-description/", views.RecommendationsByDescription.as_view(), name="by-description"),
    path("recommendations/by-id/", views.RecommendationsByMovieIds.as_view(), name="by-id"),
    path("recommendations/hybrid/", views.RecommendationsHybrid.as_view(), name="hybrid"),
]