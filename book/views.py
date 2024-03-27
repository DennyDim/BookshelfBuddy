

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView

from book.models import Book

from book.forms import BookForm

from bookie.models import BookieProfile



class BookDetailView(DetailView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_details.html'
    context_object_name = 'book'


class AddBookToWishlistView(View):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        user_profile = BookieProfile.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)
        user_profile.want_to_read.add(book)


        return redirect('book details', pk=book_id)


class AddBookToAlreadyReadView(View):

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        user_profile = BookieProfile.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)
        user_profile.have_read.add(book)

        if book in user_profile.want_to_read.all():
            user_profile.want_to_read.remove(book)

        return redirect('book details', pk=book_id)


class AddBookView(UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/add_book.html"
    success_url = reverse_lazy('main page')
    context_object_name = 'book'

    def test_func(self):
        return self.request.user.is_staff


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit_book.html'
    success_url = reverse_lazy('book details')
    context_object_name = 'book'

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.added_by or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('book details', kwargs={'pk': self.object.pk})


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('main page')

    def test_func(self):

        book = self.get_object()

        return self.request.user == book.added_by or self.request.user.is_superuser
