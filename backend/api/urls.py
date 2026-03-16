from django.urls import path
from . import views

urlpatterns = [
    # path("user-deltas/", views.UserDeltaListCreate.as_view(), name="user-delta-list"),
    path("movies/", views.DisplayMovieList.as_view(), name="movie-list"),
    path("movie/<int:pk>/", views.DisplayMovie.as_view(), name="movie"),
    path("user-actions/like/", views.LikeListCreate.as_view(), name="like"),
    path("user-actions/like/remove/<int:movie_id>/", views.LikeRemove.as_view()),
    path("user-actions/dislike/", views.DislikeListCreate.as_view(), name="like"),
    path("user-actions/dislike/remove/<int:movie_id>/", views.DislikeRemove.as_view()),
    path("user-details/", views.MeView.as_view(), name="me"),
]