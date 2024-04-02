from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView

from reviews.models import ReviewAndRating

# Create your views here.


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

            data.save()

            return redirect(current_url)
    else:
        form = ReviewForm()
        

class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReviewAndRating
    success_url = reverse_lazy('main page')


    def test_func(self):

        review = self.get_object()

        return self.request.user == review.user or self.request.user.is_staff


