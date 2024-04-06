from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from django.shortcuts import render, redirect, get_object_or_404


from bookie import forms as bookie_forms

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from bookie.models import Bookie, BookieProfile


from bookie.forms import BookieProfileForm, BookieDisplayProfileForm

# Create your views here.

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
    login_url = reverse('login bookie')
    return render(request, "bookies/delete_profile.html")


# CRUD OPERATIONS WITH THE PROFILE


class ProfileDetailView(DetailView):
    model = BookieProfile
    form_class = BookieDisplayProfileForm
    template_name = 'bookies/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):

        user_id = self.kwargs.get('pk')

        user = get_object_or_404(Bookie, id=user_id)
        profile = get_object_or_404(BookieProfile, user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.kwargs.get('pk')

        user = get_object_or_404(Bookie, id=user_id)

        context['user'] = user
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


@login_required
def delete_bookie(request, pk):

    bookie = get_object_or_404(Bookie, pk=pk)

    if request.method == 'POST':
        bookie.delete()
        return redirect('main page')

    return render(request, 'bookies/delete_profile.html')