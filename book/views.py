from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import AnonymousUser

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.views.generic.base import View

from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView, FormView
from Genre.views import get_filtered_categories

from book.forms import BookForm, BookRequestForm
from book.models import Book, BookRequestFromUserModel

from reviews.filters import FilterReviewByType
from book.filters import BookFilterByTitle


from bookie.models import BookieProfile
from reviews.models import ReviewAndRating



class BookDetailView(DetailView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books_from_the_same_series = []


        current_book = self.get_object()
        current_user = self.request.user
        all_reviews = ReviewAndRating.objects.filter(book=current_book, user=current_user)

        filter_review_by_type = FilterReviewByType(
            self.request.GET, queryset=all_reviews
        )

        all_reviews = filter_review_by_type.qs

        if current_book.name_of_series:
            books_from_the_same_series = Book.objects.filter(name_of_series=current_book.name_of_series, author=current_book.author)

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
        context['review_types'] = ReviewAndRating.TYPE_CHOICES
        context['books_from_the_same_series'] = books_from_the_same_series
        context['all_reviews'] = all_reviews
        context['filer_by_review_type'] = filter_review_by_type

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

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        name_of_series = form.cleaned_data['name_of_series']
        series_number = form.cleaned_data['series_number']
        title = form.cleaned_data['title']
        author = form.cleaned_data['author']

        if self.model.objects.filter(title=title, author=author).exists():
            raise ValidationError(f"Book: {title} by {author} already exists!")

        elif name_of_series and not series_number:
            raise ValidationError("Please provide a series number for the book.")
        elif series_number and not name_of_series:
            raise ValidationError("Please define the name of the series as well.")
        elif name_of_series and series_number and self.model.objects.filter(
            author=form.cleaned_data['author'], name_of_series=name_of_series, series_number=series_number,
                    ).exists():
            raise ValidationError(f"Book № {series_number} already added to series {name_of_series}.")

        form.instance.added_by = self.request.user
        return super().form_valid(form)


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


class BooksListView(ListView):
    model = Book
    form_class = BookForm
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)

        current_user = self.request.user
        genres = get_filtered_categories(current_user.pk)
        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )

        all_books_added = filter_by_title.qs

        context['current_user'] = current_user
        context['genres'] = genres
        context['all_books_added'] = all_books_added
        context['filter_by_title_form'] = filter_by_title

        return context


class BookRequestView(LoginRequiredMixin, FormView):
    template_name = 'books/book_request_add.html'
    form_class = BookRequestForm
    success_url = reverse_lazy('main page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def user_requests(request):
    user_requests = BookRequestFromUserModel.objects.filter(user=request.user)
    return render(request, 'books/all_user_requests.html', {'user_requests': user_requests})