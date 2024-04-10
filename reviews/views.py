from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect

from django.views.generic import DeleteView

from book.models import Book
from reviews.forms import ReviewForm
from reviews.models import ReviewAndRating


def submit_review(request, book_id):
    current_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)

            data.book_id = book_id
            data.user_id = request.user.pk
            data.has_voted = True

            data.review = form.cleaned_data['review']
            data.rating = form.cleaned_data['rating']
            data.type = form.cleaned_data['type']
            data.current_user = request.user

            data.save()

            return redirect(current_url)

    form = ReviewForm()
    current_book = Book.objects.get(id=book_id)
    context = {
        'form': form,
        'current_pk': book_id,
        'book': current_book,
    }

    return render(request, 'books/book_details.html', context)


class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReviewAndRating

    def test_func(self):
        review = self.get_object()

        return self.request.user == review.user or self.request.user.is_staff

    def get_success_url(self):
        current_url = self.request.META.get('HTTP_REFERER')
        return current_url
