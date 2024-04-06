import django_filters

from reviews import models


class FilterReviewByType(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['type'].label = ''
    class Meta:
        model = models.ReviewAndRating
        fields = ['type']




