from django.shortcuts import render
from django.views.generic import DetailView

from book.models import Book




class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_details.html'
    context_object_name = 'book'