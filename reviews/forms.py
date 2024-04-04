
from django import forms

from reviews.models import ReviewAndRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewAndRating
        fields = ['type', 'rating', 'review']

    def clean_rating(self):
        rating = self.cleaned_data['rating']

        if rating < 1 or rating > 10:
            raise forms.ValidationError('Rating must be between 1 and 10')

        return rating

