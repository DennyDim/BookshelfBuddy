
from django.core.paginator import Paginator

from django.views.generic import ListView, DetailView

from author.models import Author

from author.forms import AuthorForm, FilterAuthorsByCountry
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView


from book.models import Book




class AuthorsListView(ListView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/authors_list.html'
    context_object_name = 'authors'
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super(AuthorsListView, self).get_context_data(**kwargs)

        books_by_anonymous = Book.objects.filter(author=None)

        context['books_by_anonymous'] = books_by_anonymous

        return context


class AuthorDetailView(DetailView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/author_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        author = self.get_object()
        current_user = self.request.user

        context['authors_books'] = author.book_set.all()
        context['current_user'] = current_user

        return context


class AddAuthorView(UserPassesTestMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "authors/create_author.html"
    success_url = reverse_lazy('all_writers')

    def test_func(self):
        return self.request.user.is_staff


class AuthorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/edit_author.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('author details', kwargs={'pk': self.object.pk})


class AuthorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('all_writers')

    def test_func(self):
        return self.request.user.is_staff

