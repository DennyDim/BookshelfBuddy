

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView

from book.models import Book

from book.forms import BookForm


class BookDetailView(DetailView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_details.html'
    context_object_name = 'book'


class AddBookView(UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/add_book.html"
    success_url = reverse_lazy('main page')
    context_object_name = 'book'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.added_by = self.request.user
        self.object.save()
        form.save_m2m()

        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


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
