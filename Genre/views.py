from django.shortcuts import render


from book.models import Book

from Genre.models import Genre


# Here I filter the books and only get the appropriate books
# if the user isn`t authenticated, he can`t view books with age restriction
# if he is registered, I check his age in order to return a book
# That`s why to simplify the process, I only get the age if the user is authenticated
def get_filtered_books(books: list, age: int = None):
    filtered_books = []

    for book in books:

        # I run through each Genre to determine the minimal age required
        try:
            min_age = min([c.age_restriction for c in book.Genre.all() if c.age_restriction is not None])
        except ValueError:
            min_age = None

        # in this scenario we have age restriction and auth user
        if min_age and age:
            if min_age <= age:
                filtered_books.append(book)

        # here we simply don`t have any age restrictions
        elif min_age is None:
            filtered_books.append(book)

    return filtered_books


# Here I filter the categories
def get_filtered_categories(age: int = None):
    genres = Genre.objects.all()
    filtered_categories = []

    for genre in genres:
        if genre.age_restriction and age:
            # I get only the categories that are available to the auth user
            if genre.age_restriction <= age:
                filtered_categories.append(Genre)

        # And here I just get the categories without age restriction. They are available to anyone.
        elif not genre.age_restriction:
            filtered_categories.append(Genre)

    return filtered_categories


def main_page(request):
    filtered_categories = []
    total_books = []

    if request.user.is_staff:
        total_books = Book.objects.all()
    else:
        user_age = None
        if request.user.is_authenticated:
            user_age = request.user.age

        filtered_categories = get_filtered_categories(user_age)
        total_books = Book.objects.all().count()

    context = {
        'total_books': total_books,
    }
    if not request.user.is_staff:
        context['categories'] = filtered_categories

    return render(request, "main_page.html", context)
