from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse

from django.shortcuts import render, redirect

from bookie import forms as bookie_forms

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from bookie.models import Bookie, BookieProfile

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


def logout_view(request):
    logout(request)
    login_url = reverse('login bookie')  # Get the URL for 'login bookie'
    return HttpResponse(f"You have been logged out successfully. <a href='{login_url}'>That's fine</a>")


class ProfileDetailView(DetailView):
    model = BookieProfile
    template_name = 'bookies/profile.html'
    context_object_name = 'profile'


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookieProfile
    fields = ['profile_picture', 'bio', 'books_i_want_to_read', 'books_ive_read']
    template_name = 'bookies/edit_profile.html'
    success_url = reverse_lazy('bookie profile')

    def test_func(self):
        return self.request.user == self.get_object().user


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookieProfile
    template_name = 'bookies/delete_profile.html'
    success_url = reverse_lazy('main page')

    def test_func(self):
        return self.request.user == self.get_object().user

    def delete(self, request, *args, **kwargs):

        user = self.get_object().user
        self.object = self.get_object()

        success_url = self.get_success_url()

        self.object.delete()
        user.delete()
        return redirect(success_url)
