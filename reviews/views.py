from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from reviews.models import ReviewAndRating
from reviews.forms import ReviewForm

# Create your views here.


def submit_review(request, book_id):
    current_url = request.META.get('HTTP_REFERER')


    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print('Form data:', form.cleaned_data)
            data = form.save(commit=False)
            data.book_id = book_id
            data.user_id = request.user.id
            data.has_voted = True
            data.review = form.cleaned_data['review']
            data.rating = form.cleaned_data['rating']

            data.save()

            messages.success(request, 'Thank you for your review!')
            return redirect(current_url)
        else:
            print("Form errors:", form.errors)


class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReviewAndRating
    success_url = reverse_lazy('main page')

    def test_func(self):

        review = self.get_object()

        return self.request.user == review.user or self.request.user.is_staff


"""
                data = ReviewForm()
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.book_id = book_id
                data.user_id = request.user.pk
                data.has_voted = True

                data.save()
                """