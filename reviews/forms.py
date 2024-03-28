
from django import forms

from reviews.models import ReviewAndRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewAndRating
        fields = ['rating', 'review', 'has_voted']
