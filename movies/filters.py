import django_filters

from movies.models import Movie, Genre


class MovieFilter(django_filters.FilterSet):
    genres = django_filters.ModelChoiceFilter(queryset=Genre.objects.all(), label='Genre')
    actor = django_filters.CharFilter(field_name='actor__name', lookup_expr='icontains', label='Actor')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains', label='description')

    class Meta:
        model = Movie
        fields = ['genres', 'actor', 'description']