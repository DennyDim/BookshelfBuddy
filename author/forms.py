
from django import forms

from author.models import Author, Country
from book.models import Book


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('name', '') == 'Unknown':
            raise forms.ValidationError("Cannot delete the 'Unknown' country.")
        return cleaned_data


class AuthorForm(forms.ModelForm):

    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=True)

    class Meta:

        model = Author
        fields = ['name', 'pseudonym', 'year_born','country', 'author_picture', 'authors_bio']

        min_year_born = Author.MIN_YEAR_BORN
        super_user_email = Book.SUPER_USER_EMAIL
    
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Author`s name...',
                       'autofocus': True,}
            ),

            'pseudonym': forms.TextInput(
                attrs={'placeholder': 'Does the author have a pseudonym?'}
            ),

            'authors_bio': forms.Textarea(
                attrs={'placeholder': 'Quick and easy to read bio about the author...'}
            )
        }

        error_messages = {
            'name':
                {'unique': 'An author with this name already exists.'}
        }

        help_texts = {
            'year_born': f'If the author you want to add was born before year {min_year_born}\n'
                         f', please contact the admin at {super_user_email}.'
        }


class FilterAuthorsByCountry(forms.Form):

    countries = Country.objects.values_list('name', flat=True).distinct()
    country_choices = [(country, country) for country in countries]
    country = forms.ChoiceField(choices=country_choices, label='Select a country')
