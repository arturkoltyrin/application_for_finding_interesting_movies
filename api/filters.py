from django_filters import rest_framework as filters

from movies.models import Actor, Genre, Movie
from users.models import User


class GenreFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Genre
        fields = ["name"]


class ActorFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    surname = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Actor
        fields = ["name", "surname"]


class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    actor = filters.CharFilter(field_name="actor__name", lookup_expr="icontains")
    actor_id = filters.NumberFilter(field_name="actor__id")
    genres = filters.CharFilter(method="filter_by_genre_name")
    genre_id = filters.NumberFilter(field_name="genres__id")

    def filter_by_genre_name(self, queryset, name, value):
        return queryset.filter(genres__name__icontains=value)

    class Meta:
        model = Movie
        fields = ["title", "description", "actor", "genres"]


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr="icontains")
    preferred_genres = filters.ModelChoiceFilter(
        field_name="preferred_genres__name",
        queryset=Genre.objects.all(),
        lookup_expr="icontains",
    )

    class Meta:
        model = User
        fields = ["email", "preferred_genres"]
