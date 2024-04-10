from django import forms

from book.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'year_published', 'cover_image', 'description', 'name_of_series',
                  'series_number', ]

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter book title...'},
            ),
            'genres': forms.CheckboxSelectMultiple(),
        }

        help_texts = {
            'author': 'If you can`t find the author of this book,\n'
                      ' please create it first then add the book.'
        }


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'year_published', 'cover_image', 'description', ]

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter book title...'},
            ),
            'genres': forms.CheckboxSelectMultiple(),
        }

        help_texts = {
            'author': 'If you can`t find the author of this book,\n'
                      ' please create it first then add the book.'
        }
