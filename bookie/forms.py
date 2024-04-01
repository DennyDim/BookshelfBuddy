from django.contrib.auth import forms as auth_forms
from django import forms
from django.core.validators import MinValueValidator

from bookie.models import Bookie, BookieProfile

from bookie import validators as bookie_validators


class BookieRegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = Bookie
        fields = ('email', 'age', 'password1', 'password2')

        MIN_PASSWORD_LENGTH = 6
        MIN_LEN_NUMBERS = 2

        labels = {
            'password1': 'Create stable password',
            'password2': 'Re-enter your password',
        }

        help_texts = {
            'age': 'This field is important for our site.',
            'password1': f"~ Your password must be at least {MIN_PASSWORD_LENGTH} characters long! <br>"
                         f"~ Your password must have at least {MIN_LEN_NUMBERS} digits!",
        }

        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'autofocus': True,
            }),

            'password1': forms.PasswordInput(
            ),

            'password2': forms.PasswordInput()
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['password1'].validators.append(bookie_validators.CustomLengthValidator)
            self.fields['password1'].validators.append(bookie_validators.CustomNumberValidator)


class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': 'Please make sure the credentials are valid. Both fields are case-sensitive.',
        'inactive': 'This profile has been deactivated.'
    }


class LogInBookieForm(CustomAuthenticationForm):
    class Meta:
        model = Bookie
        fields = ('email', 'password')

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
        fields = ['profile_picture', 'username', 'bio']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Create a unique name for yourself. |form',
                                               'autofocus': True},
                                        )
            ,
            'bio': forms.Textarea(
                attrs={'placeholder': 'Share something about yourself! |form'}
            )
        }
