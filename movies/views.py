from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from interactions.forms import RatingForm
from interactions.models import Interaction
from movies.filters import MovieFilter
from movies.forms import ActorForm, GenreForm, MovieForm
from movies.models import Actor, Genre, Movie
from recommendations.services import (
    get_collaborative_recommendations_service,
    get_pagerank_recommendations_service, get_statistics)


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class HomeView(TemplateView):
    template_name = "movies/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GenreListView(StaffRequiredMixin, ListView):
    model = Genre
    template_mame = "movies/genre_list.html"
    context_object_name = "genres"
    paginate_by = 10


class GenreDetailView(StaffRequiredMixin, DetailView):
    model = Genre
    template_name = "movies/genre_detail.html"
    context_object_name = "genre"


class GenreCreateView(StaffRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = "movies/genre_form.html"
    success_url = reverse_lazy("movies:genres")


class GenreUpdateView(StaffRequiredMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = "movies/genre_form.html"
    success_url = reverse_lazy("movies:genres")


class GenreDeleteView(StaffRequiredMixin, DeleteView):
    model = Genre
    template_name = "movies/genre_confirm_delete.html"
    success_url = reverse_lazy("movies:genres")


class ActorListView(StaffRequiredMixin, ListView):
    model = Actor
    template_name = "movies/actor_list.html"
    context_object_name = "actors"
    paginate_by = 10


class ActorDetailView(StaffRequiredMixin, DetailView):
    model = Actor
    template_name = "movies/actor_detail.html"
    context_object_name = "actor"


class ActorCreateView(StaffRequiredMixin, CreateView):
    model = Actor
    form_class = ActorForm
    template_name = "movies/actor_form.html"
    success_url = reverse_lazy("movies:actors")


class ActorUpdateView(StaffRequiredMixin, UpdateView):
    model = Actor
    form_class = ActorForm
    template_name = "movies/actor_form.html"
    success_url = reverse_lazy("movies:actors")


class ActorDeleteView(StaffRequiredMixin, DeleteView):
    model = Actor
    template_name = "movies/actor_confirm_delete.html"
    success_url = reverse_lazy("movies:actors")


class MovieListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    context_object_name = "movies"
    paginate_by = 10
    filterset_class = MovieFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("q", "")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(actor__name__icontains=search_query)
                | Q(description__icontains=search_query)
            )
        genre_filter = self.request.GET.get("genres", "")
        if genre_filter:
            queryset = queryset.filter(genres__id=genre_filter)
        ordering = self.request.GET.get("sort", "-publish_date")
        allowed_sort_fields = [
            "title",
            "-title",
            "publish_date",
            "-publish_date",
            "rating",
            "-rating",
        ]
        if ordering in allowed_sort_fields:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = MovieFilter(self.request.GET, queryset=self.get_queryset())
        return context


@method_decorator(login_required, name="dispatch")
class MovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"

    def get_queryset(self):
        return super().get_queryset().select_related("some_related_field")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        interaction = Interaction.objects.filter(
            user=self.request.user, movie=movie
        ).first()
        context["rating_form"] = RatingForm(instance=interaction)
        context["user_rating"] = interaction.rating if interaction else None
        return context

    def post(self, request, *args, **kwargs):
        movie = self.get_object()
        interaction, created = Interaction.objects.get_or_create(
            user=request.user, movie=movie
        )
        form = RatingForm(request.POST, instance=interaction)
        if form.is_valid():
            form.save()
        return redirect("movies:movie-detail", pk=movie.pk)


class MovieCreateView(StaffRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "movies/movie_form.html"
    success_url = reverse_lazy("movies:movies")


class MovieUpdateView(StaffRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "movies/movie_form.html"
    success_url = reverse_lazy("movies:movies")


class MovieDeleteView(StaffRequiredMixin, DeleteView):
    model = Movie
    template_name = "movies/movie_confirm_delete.html"
    success_url = reverse_lazy("movies:movies")


class StatisticsView(TemplateView):
    template_name = "movies/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics_data = get_statistics()
        context["movies_count"] = statistics_data["movies_count"]
        context["users_count"] = statistics_data["users_count"]
        context["new_movies_week_count"] = statistics_data["new_movies_week_count"]
        context["top_rated_movies"] = statistics_data["top_rated_movies"]
        context["top_active_users"] = statistics_data["top_active_users"]

        return context


class RecommendationView(LoginRequiredMixin, TemplateView):
    template_name = "movies/recommendations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context["pagerank_recommendations"] = get_pagerank_recommendations_service(
            user_id
        )
        context["collaborative_recommendations"] = (
            get_collaborative_recommendations_service(user_id)
        )

        return context
