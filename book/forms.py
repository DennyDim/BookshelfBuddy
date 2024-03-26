
from django import forms



from book.models import Book, Category


class BookForm(forms.ModelForm):


    class Meta:
        model = Book
        fields = ['title', 'author', 'categories', 'year_published','cover_image', 'description']

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter book title...'},
            ),
            'categories': forms.CheckboxSelectMultiple(),
            }

        error_messages = {
            'title':
                {'unique': 'Sorry, someone has already added this book.'}
        }

        help_texts = {
            'author': 'If you can`t find the author of this book,\n'
                      ' please create it first then add the book.'
        }

