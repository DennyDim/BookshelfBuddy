from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.exceptions import ValidationError
from django.db.models import Q, Count, Avg

from django.shortcuts import redirect, render, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic.base import View

from django.views.generic import DetailView, UpdateView, CreateView, ListView
from Genre.views import show_genre
from author.models import Author

from book.forms import BookForm, BookUpdateForm
from book.models import Book

from reviews.filters import FilterReviewByType
from book.filters import BookFilterByTitle

from bookie.models import BookieProfile, Bookie

from datetime import datetime

from reviews.models import ReviewAndRating


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
        form.instance.added_on_date = datetime.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )
        context['filter_by_title_form'] = filter_by_title
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = 'books/edit_book.html'
    success_url = reverse_lazy('book details')
    context_object_name = 'book'

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.added_by or self.request.user.is_superuser

    def form_valid(self, form):
        current_title = form.cleaned_data['title']
        current_author = form.cleaned_data['author']

        if Book.objects.filter(title=current_title, author=current_author).count() > 1:
            raise ValueError(f"Book {current_title} bt {current_author} has been added already.")

        form.instance.last_edited_on_date = datetime.now()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )
        context['filter_by_title_form'] = filter_by_title
        return context


@login_required()
def delete_book(request, pk):
    context = {
        'current_pk': pk
    }

    if request.method == "POST":
        if request.user.is_authenticated:
            current_book = get_object_or_404(Book, pk=pk)

            current_book.delete()

            return redirect('main page')

    return render(request, 'books/delete_book.html', context)


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

        current_review = None

        all_reviews = ReviewAndRating.objects.filter(book=current_book)

        filter_review_by_type = FilterReviewByType(
            self.request.GET, queryset=all_reviews
        )

        all_reviews = filter_review_by_type.qs

        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )

        if current_book.name_of_series:
            books_from_the_same_series = Book.objects.filter(name_of_series=current_book.name_of_series,
                                                             author=current_book.author)

        try:
            current_review = ReviewAndRating.objects.get(book=current_book, user=current_user)

        except ReviewAndRating.DoesNotExist:
            pass

        except TypeError:
            pass

        context['book'] = self.get_object()
        context['current_user'] = current_user

        context['current_review'] = current_review
        context['filer_by_review_type'] = filter_review_by_type
        context['review_types'] = ReviewAndRating.TYPE_CHOICES
        context['books_from_the_same_series'] = books_from_the_same_series
        context['all_reviews'] = all_reviews
        context['filter_by_title_form'] = filter_by_title

        return context


class MainPage(ListView):
    model = Book
    form_class = BookForm
    template_name = 'main_page.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        current_user = None

        try:
            current_user = self.request.user

        except Bookie.DoesNotExist:
            current_user = Bookie.DoesNotExist

        genres = show_genre(current_user)

        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )

        search_results = filter_by_title.qs

        top_10_authors = Author.objects.annotate(likes=Count('people_who_like_this_author')).order_by('-likes', 'name')[
                         :10]
        top_10_rated_books = (
            Book.objects
            .annotate(avg_rating=Avg('book_reviews__rating'))
            .order_by('-avg_rating', 'title')
            [:10]
        )

        last_3_added_books = Book.objects.order_by("-added_on_date")[:3]

        context['current_user'] = current_user
        context['genres'] = genres
        context['all_books_added'] = all_books_added
        context['filter_by_title_form'] = filter_by_title
        context['search_results'] = search_results

        context['top_10_authors'] = top_10_authors
        context['best_rated_books'] = top_10_rated_books
        context['last_3_added_books'] = last_3_added_books

        return context


class BooksListViewInGenre(ListView):
    model = Book
    form_class = BookForm
    template_name = 'books/genre_book_list.html'
    context_object_name = "genre_books"
    ordering = ['title']
    paginate_by = 5

    def get_queryset(self):
        genre_name = self.kwargs.get('genre')

        queryset = Book.objects.filter(genres__name=genre_name).order_by('title')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_name = self.kwargs.get('genre')
        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            self.request.GET,
            queryset=all_books_added
        )
        context['filter_by_title_form'] = filter_by_title

        context['genre_name'] = genre_name

        return context


class AddBookToAlreadyReadView(View):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        user_profile = BookieProfile.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)
        user_profile.have_read.add(book)

        if book in user_profile.want_to_read.all():
            user_profile.want_to_read.remove(book)

        return redirect('book details', pk=book_id)


class AddBookToWishlistView(View):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        user_profile = BookieProfile.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)
        user_profile.want_to_read.add(book)

        return redirect('book details', pk=book_id)


@login_required
def generate_random_book(request):
    current_user = request.user

    books_we_can_generate = Book.objects.exclude(
        Q(have_read__user=current_user) | Q(want_to_read__user=current_user)
    )

    all_books_added = Book.objects.all()

    filter_by_title = BookFilterByTitle(
        request.GET,
        queryset=all_books_added
    )

    context = {
        'filter_by_title_form': filter_by_title
    }

    if books_we_can_generate.exists():
        random_book = books_we_can_generate.order_by("?").first()

        context['book'] = random_book
        context['current_user'] = current_user

        return render(request, 'books/random_book.html', context)

    return redirect('no random')


def search_view(request):
    super_user_pk = Bookie.SUPERUSER_PK

    if request.method == "POST":

        book_filter = BookFilterByTitle(request.POST, queryset=Book.objects.all())

        all_books_added = Book.objects.all()

        filter_by_title = BookFilterByTitle(
            request.GET,
            queryset=all_books_added
        )

        if book_filter.form.is_valid():
            search_results = book_filter.qs

            context = {
                'search_results': search_results,
                'filter_by_title_form': filter_by_title
            }

            return render(request, 'search_results.html', context)

    context = {
        'filter_by_title_form': filter_by_title,
        'super_user_pk': super_user_pk,

    }
    return render(request, 'base.html', context)


def get_no_random_template(request):
    all_books_added = Book.objects.all()

    filter_by_title = BookFilterByTitle(
        request.GET,
        queryset=all_books_added
    )
    context = {
        'filter_by_title_form': filter_by_title
    }

    return render(request, 'no_book/no_random_book.html', context)


def about_us_page(request):
    all_books_added = Book.objects.all()
    super_user_email = Book.SUPER_USER_EMAIL
    super_user_pk = Book.SUPERUSER_PK

    filter_by_title = BookFilterByTitle(
        request.GET,
        queryset=all_books_added
    )
    context = {
        'filter_by_title_form': filter_by_title,
        'super_user_email': super_user_email,
        'super_user_pk': super_user_pk
    }

    return render(request, 'about_page.html', context)
