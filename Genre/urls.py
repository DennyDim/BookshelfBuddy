
from django.urls import path

from book import views as book_views


urlpatterns = [
    path("", book_views.BooksListView.as_view(), name="main page"),
]