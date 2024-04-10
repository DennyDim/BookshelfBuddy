
import django_filters

from django import forms
from book.models import Book
from django_filters import CharFilter


class BookFilterByTitle(django_filters.FilterSet):
    title = CharFilter(
        field_name="title",
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput
        (attrs={'placeholder': 'Enter book title...'}))

    class Meta:
        model = Book
        fields = ['title']

