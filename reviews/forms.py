
from django import forms

from reviews.models import ReviewAndRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewAndRating
        fields = ['rating', 'review', 'has_voted']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].required = True
