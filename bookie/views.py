from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from bookie import forms as bookie_forms


# Create your views here.


def main_page(request):

    text = "This is the main page"

    user = request.user

    context = {
        "text": text,
        "user": user
    }
    return render(request, "main_page.html", context)


class RegisterBookieView(CreateView):
    template_name = "bookies/registration.html"
    form_class = bookie_forms.BookieRegistrationForm
    success_url = reverse_lazy("login bookie")


class BookieLoginView(LoginView):
    template_name = "bookies/log_in.html"
    form_class = bookie_forms.LogInBookieForm
    success_url = reverse_lazy("main page")


class BookieLogoutView(LogoutView):
    next_page = "main page"


class BookieProfile(DetailView):
    model = get_user_model()
    template_name = "bookies/profile.html"
    context_object_name = "user"


class BookieProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = bookie_forms.BookieProfile
    template_name = "bookies/edit_profile.html"
    success_url = reverse_lazy("bookie profile")