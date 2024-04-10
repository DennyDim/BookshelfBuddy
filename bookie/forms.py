from django.contrib.auth import forms as auth_forms
from django import forms
from django.contrib.auth.forms import UserCreationForm


from bookie.models import Bookie, BookieProfile




class BookieRegistrationForm(auth_forms.UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Bookie
        fields = ['email', 'age', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address',
            'autofocus': True,
        })

        self.fields['password1'].label = 'Create a stable password:'
        self.fields['password2'].label = 'Re-enter your password:'



class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': 'Please make sure the credentials are valid. Both fields are case-sensitive.',
        'inactive': 'This profile has been deactivated.'
    }


class LogInBookieForm(CustomAuthenticationForm):
    class Meta:
        model = Bookie
        fields = ['email', 'password']

        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address...',
                'autofocus': True}
            ),

            'password': forms.CharField(

                label='Enter your password',
                strip=False,
                widget=forms.PasswordInput()),

        }


class BookieProfileForm(forms.ModelForm):
    class Meta:
        model = BookieProfile
        fields = ['profile_picture', 'country', 'bio',]

        widgets = {
            'bio': forms.Textarea(
                attrs={'placeholder': 'Share something about yourself!'}
            ),
            'country': forms.TextInput(
                attrs={'placeholder': 'Share where you come from...'}
            )
        }


class BookieDisplayProfileForm(forms.ModelForm):
    class Meta:
        model = BookieProfile
        fields = ['profile_picture', 'bio', 'country', 'have_read', 'want_to_read']


class DeleteBokieForm(forms.Form):
    class Meta:
        model = Bookie
        fields =('__all__')
