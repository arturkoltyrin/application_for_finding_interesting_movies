from django import forms

from movies.models import Genre, Actor, Movie


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GenreForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', ]


class ActorForm(StyleFormMixin, forms.ModelForm):
    surname = forms.CharField(required=False)

    class Meta:
        model = Actor
        fields = ['name', 'surname']


class MovieForm(StyleFormMixin, forms.ModelForm):
    cover = forms.ImageField(required=False, label='Cover')
    actor = forms.ModelChoiceField(
        queryset=Actor.objects.all(),
        label='Actor')
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Genres')

    class Meta:
        model = Movie
        fields = ['title', 'cover', 'actor', 'description', 'genres']