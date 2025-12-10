from django.urls import path
from . import views

urlpatterns = [
    path("user-deltas/", views.UserDeltaListCreate.as_view(), name="user-delta-list"),
    # path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("movies/", views.DisplayMovieList.as_view(), name="movie-list"),
    path("movie/<int:pk>/", views.DisplayMovie.as_view(), name="movie"),
    path("user-actions/like/", views.LikeListCreate.as_view(), name="like"),
]