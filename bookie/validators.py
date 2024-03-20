
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

from django.utils.translation import gettext_lazy as _


class CustomLengthValidator(BaseValidator):

    # The current min length is 6
    def __init__(self, min_length):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f"Your password is too short. Must contain at least {self.min_length} characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_message(self):
        return f"~ You password mst contain at least {self.min_length} characters"


class CustomNumberValidator(BaseValidator):

    # the current min len numbers is 2
    def __init__(self, min_len_numbers):
        self.min_len_numbers = min_len_numbers

    def validate(self, password, user=None):
        all_numbers = [el for el in password if el.isdigit()]
        if len(all_numbers) < self.min_len_numbers:
            raise ValidationError(
                _(f"The password must contain at least {self.min_len_numbers} digits."),
                code='not_enough_numbers',
                params={'min_length': self.min_len_numbers},
            )

    def get_help_message(self):
        return f"~ Your password must contain at least {self.min_len_numbers} digits."