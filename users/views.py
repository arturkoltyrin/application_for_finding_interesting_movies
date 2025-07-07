from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, UpdateView

from interactions.models import Interaction
from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Successful registration")
        return response


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def form_valid(self, form):
        from django.contrib.auth import login

        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"Welcome {user.email}!")
        return super().form_valid(form)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"
    slug_field = None

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ratings"] = Interaction.objects.filter(
            user=self.request.user
        ).select_related("movie")
        return context


def my_profile_redirect(request):
    return redirect(reverse("users:profile", kwargs={"pk": request.user.pk}))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={"pk": self.request.user.pk})

    def test_func(self):
        return self.get_object() == self.request.user

    def get_object(self, queryset=None):
        return self.request.user
