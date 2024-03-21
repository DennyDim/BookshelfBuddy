from django.shortcuts import render

from category import views as category_views

from django.views.generic import ListView, DetailView

from .models import Author


class AuthorsListView(ListView):
    model = Author
    template_name = 'authors/authors_list.html'
    context_object_name = 'authors'
    ordering = ['name']


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'authors/author_profile.html'
    context_object_name = 'author'


