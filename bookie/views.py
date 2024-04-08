from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator

from bookie import forms as bookie_forms

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from bookie.models import Bookie, BookieProfile


from bookie.forms import BookieProfileForm, BookieDisplayProfileForm
from datetime import datetime

from bookie.decorators import allowed_users, custom_login_required


class RegisterBookieView(CreateView):
    template_name = "bookies/registration.html"
    form_class = bookie_forms.BookieRegistrationForm
    success_url = reverse_lazy("login bookie")

    def form_valid(self, form):

        form.instance.date_joined = datetime.now()

        return super().form_valid(form)


class BookieLoginView(LoginView):
    template_name = "bookies/log_in.html"
    form_class = bookie_forms.LogInBookieForm
    success_url = reverse_lazy("main page")



def logout_view(request):
    logout(request)
    return redirect("login bookie")


class ProfileDetailView(DetailView):
    model = BookieProfile
    form_class = BookieDisplayProfileForm
    template_name = 'bookies/profile.html'

    def get_object(self, queryset=None):

        user_id = self.kwargs.get('pk')

        user = get_object_or_404(Bookie, id=user_id)
        profile = get_object_or_404(BookieProfile, user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user
        users_profile_pk = self.kwargs.get('pk')

        current_profile = BookieProfile.objects.get(pk=users_profile_pk)
        current_profile_email = Bookie.objects.get(pk=users_profile_pk)

        context['current_user'] = current_user
        context['current_profile'] = current_profile
        context['current_email'] = current_profile_email.email
        return context



class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookieProfile
    form_class = BookieProfileForm
    template_name = 'bookies/edit_profile.html'
    success_url = reverse_lazy('bookie profile')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(BookieProfile, pk=pk)

    def get_success_url(self):
        return reverse_lazy('bookie profile', kwargs={'pk': self.object.pk})

    def test_func(self):

        return self.request.user.pk == self.kwargs.get('pk') or self.request.user.is_superuser



class DeleteBookie(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bookie
    success_url = reverse_lazy('main page')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context

def not_allowed_page(request):
    return render(request, 'errors/not_allowed.html')

