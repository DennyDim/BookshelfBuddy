from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView

from book.forms import BookForm
from book.models import Book



from bookie.models import BookieProfile, Bookie
from reviews.models import ReviewAndRating



class BookDetailView(DetailView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_book = self.get_object()
        current_user = self.request.user

        if isinstance(current_user, AnonymousUser):
            current_review = None

        else:
            try:
                current_review = ReviewAndRating.objects.get(book=current_book, user=current_user)

            except ReviewAndRating.DoesNotExist:
                current_review = None

        context['book'] = self.get_object()
        context['current_user'] = current_user
        context['current_review'] = current_review
        return context


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
