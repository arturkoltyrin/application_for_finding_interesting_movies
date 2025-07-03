from django.urls import path
from movies.apps import MoviesConfig
from movies.views import HomeView, GenreListView, GenreDetailView, GenreCreateView, GenreUpdateView, ActorListView, \
    ActorDetailView, ActorCreateView, ActorUpdateView, ActorDeleteView, MovieCreateView, MovieDetailView, \
    MovieListView, GenreDeleteView, MovieUpdateView, MovieDeleteView, StatisticsView, RecommendationView

app_name = MoviesConfig.name

urlpatterns = [
    path('actors/', ActorListView.as_view(), name='actors'),
    path('actors/<int:pk>/', ActorDetailView.as_view(), name='actor-detail'),
    path('actors/new/', ActorCreateView.as_view(), name='actor-create'),
    path('actors/<int:pk>/edit/', ActorUpdateView.as_view(), name='actor-update'),
    path('actors/<int:pk>/delete/', ActorDeleteView.as_view(), name='actor-delete'),
    path('genres/', GenreListView.as_view(), name='genres'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    path('genres/new/', GenreCreateView.as_view(), name='genre-create'),
    path('genres/<int:pk>/edit/', GenreUpdateView.as_view(), name='genre-update'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre-delete'),
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/new/', MovieCreateView.as_view(), name='movie-create'),
    path('movies/<int:pk>/edit/', MovieUpdateView.as_view(), name='movie-update'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie-delete'),
    path('', HomeView.as_view(), name='home'),
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('statistics/', StatisticsView.as_view(), name='statistics')]