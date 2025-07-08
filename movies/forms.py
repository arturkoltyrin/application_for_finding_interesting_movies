from django import forms

from movies.models import Actor, Genre, Movie


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs["class"] = "form-control"


class GenreForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Genre
        fields = [
            "name",
        ]


class ActorForm(StyleFormMixin, forms.ModelForm):
    surname = forms.CharField(required=False)

    class Meta:
        model = Actor
        fields = ["name", "surname"]


class MovieForm(StyleFormMixin, forms.ModelForm):
    cover = forms.ImageField(required=False, label="Cover")
    actor = forms.ModelChoiceField(queryset=Actor.objects.all(), label="Actor")
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Genres",
    )

    class Meta:
        model = Movie
        fields = ["title", "cover", "actor", "description", "genres"]
