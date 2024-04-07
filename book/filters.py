
import django_filters

from book.models import Book
from django_filters import CharFilter


class BookFilterByTitle(django_filters.FilterSet):
    title = CharFilter(
        field_name="title",
        lookup_expr='icontains',
        label='Search for book by title:')

    class Meta:
        model = Book
        fields = ['title']