
from django.contrib.auth import forms as auth_forms
from django import forms


from bookie.models import Bookie, BookieProfile



class BookieRegistrationForm(auth_forms.UserCreationForm):

    class Meta:
        model = Bookie
        fields = ('username', "email", "password1", "password2", 'age')

    def __init__(self, *args, **kwargs):

        MIN_PASSWORD_LENGTH = 6
        MIN_LEN_NUMBERS = 2

        super(BookieRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Create unique name for yourself!',
            'autofocus': True,
        })
        self.fields['username'].help_text = "You can use anything you want!"

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address...'
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create stable password...',
        })

        self.fields['password1'].help_text = f"~ Your password must be at least {MIN_PASSWORD_LENGTH} characters long!"
        self.fields['password1'].help_text += "<br>"
        self.fields['password1'].help_text += f"~ Your password must have at least {MIN_LEN_NUMBERS} digits!"

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Re-enter your password...',

        })

        self.fields['age'].help_text = "This field is important for our site."


class LogInBookieForm(auth_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs["placeholder"] = "Enter your username..."
        self.fields['username'].widget.attrs["autofocus"] = True

        self.fields["password"].widget.attrs["placeholder"] = "Enter your password..."



class BookLibraryForm(forms.Form):
    book_id = forms.IntegerField()
    library_type = forms.ChoiceField(choices=(('want_to_read', 'Want to Read'), ('have_read', 'Have Read')))

