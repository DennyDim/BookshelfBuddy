
from django.core.paginator import Paginator

from django.views.generic import ListView, DetailView

from author.models import Author

from author.forms import AuthorForm, FilterAuthorsByCountry
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView

from book.filters import BookFilterByTitle
from book.models import Book




class AuthorsListView(ListView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/authors_list.html'
    context_object_name = 'authors'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )
        context['filter_by_title_form'] = filter_by_title
        return context



class AuthorDetailView(DetailView):

    model = Author
    form_class = AuthorForm
    template_name = 'authors/author_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        author = self.get_object()
        current_user = self.request.user
        all_likes = author.people_who_like_this_author.all()

        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
            )
        context['filter_by_title_form'] = filter_by_title
        context['all_likes'] = all_likes

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )
        context['filter_by_title_form'] = filter_by_title
        return context


class AuthorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/edit_author.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )
        context['filter_by_title_form'] = filter_by_title
        return context

    def get_success_url(self):
        return reverse_lazy('author details', kwargs={'pk': self.object.pk})


class AuthorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('all_writers')

    def test_func(self):
        return self.request.user.is_staff


def like_author(request, pk):

    current_page = request.META.get('HTTP_REFERER')
    author = Author.objects.get(pk=pk)

    if request.user.is_authenticated:
        if request.user not in author.people_who_like_this_author.all():
            author.people_who_like_this_author.add(request.user)

    return redirect(current_page)
