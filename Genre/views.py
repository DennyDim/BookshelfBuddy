from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from book.models import Book

from Genre.models import Genre

from bookie.models import Bookie



# Here I filter the books and only get the appropriate books
# if the user isn`t authenticated, he can`t view books with age restriction
# if he is registered, I check his age in order to return a book
# That`s why to simplify the process, I only get the age if the user is authenticated



# Here I filter the categories
def get_filtered_categories(user_id: int):

    genres = Genre.objects.all()
    user = get_object_or_404(Bookie, pk=user_id)

    if user.is_authenticated:
        if user.is_staff:
            filtered_categories = genres
        else:
            filtered_categories = genres.filter(Q(age_restriction__lte=user.age)| Q(age_restriction__isnull=True))
    else:
        filtered_categories = genres.filter(age_restriction__isnull=True)

    return filtered_categories


def main_page(request):

    genres = get_filtered_categories(request.user.pk)
    all_books_added = Book.objects.all()



    current_user = request
    context = {
        'current_user': current_user,
        'genres': genres,
        'all_books_added': all_books_added,

    }

    return render(request, "main_page.html", context)
