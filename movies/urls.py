from django.urls import path
from .views import MoviesView, MoviesDatailView, MovieOrderDetailView

urlpatterns = [
    path('movies/', MoviesView.as_view()),
    path('movies/<int:movie_id>/', MoviesDatailView.as_view()),
    path('movies/<int:movie_id>/orders/', MovieOrderDetailView.as_view()),
]