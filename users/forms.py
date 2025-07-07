from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

import movies
from movies.forms import StyleFormMixin
from movies.models import Genre
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    avatar = forms.ImageField(required=False, label="Avatar")
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=movies.models.Genre.objects.all(),
        required=False,
        label="Preferred Genres",
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "avatar", "preferred_genres")


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class UserUpdateForm(forms.ModelForm):
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = ["email", "avatar", "preferred_genres"]
