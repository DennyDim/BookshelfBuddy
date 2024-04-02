from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from bookie import forms as bookie_forms

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from bookie.models import Bookie, BookieProfile


from bookie.forms import BookieProfileForm, BookieDisplayProfileForm

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


# CRUD OPERATIONS WITH THE PROFILE


class ProfileDetailView(DetailView):
    model = BookieProfile
    form_class = BookieDisplayProfileForm
    template_name = 'bookies/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):

        profile = get_object_or_404(BookieProfile, user=self.request.user)

        if profile.user != self.request.user:
            raise PermissionDenied

        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['user'] = self.request.user
        context['profile'] = self.get_object()
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookieProfile
    form_class = BookieProfileForm
    template_name = 'bookies/edit_profile.html'
    success_url = reverse_lazy('bookie profile')

    def get_object(self, queryset=None):
        return get_object_or_404(BookieProfile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('bookie profile', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user == self.get_object().user or self.request.user.is_superuser


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bookie
    template_name = 'bookies/delete_profile.html'
    context_object_name = 'user to delete'
    success_url = reverse_lazy('login bookie')

    def test_func(self):

        user = self.get_object()

        return self.request.user == user or self.request.user.is_superuser

    def get_object(self, queryset=None):
        return get_object_or_404(Bookie, pk=self.request.user.pk)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.delete()
        return reverse_lazy(success_url)