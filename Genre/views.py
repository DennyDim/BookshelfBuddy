from django.db.models import Q

from Genre.models import Genre

from bookie.models import Bookie

import datetime


# Here I filter the books and only get the appropriate books
# if the user isn`t authenticated, he can`t view books with age restriction
# if he is registered, I check his age in order to return a book
# That`s why to simplify the process, I only get the age if the user is authenticated


# Here I filter the categories

def show_genre(bookie: Bookie):
    user = bookie
    today = datetime.date.today()

    if user.is_authenticated:

        if user.is_staff:

            genres = Genre.objects.all()

        else:
            user_age = (today.year - user.date_joined.year) + user.age

            genres = Genre.objects.filter(Q(age_restriction__lte=user_age) | Q(age_restriction__isnull=True))

    else:
        genres = Genre.objects.filter(age_restriction__isnull=True)

    return genres
