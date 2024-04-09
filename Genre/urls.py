
from django.urls import path

from book import views as book_views


urlpatterns = [
    path("", book_views.MainPage.as_view(), name="main page"),

    path('genre/<str:name>', book_views.BooksListViewInGenre.as_view(), name='all_books'),

    path("genre/<str:genre>/<int:page>/", book_views.BooksListViewInGenre.as_view(), name='paginated books')
]