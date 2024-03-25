
from django.urls import path, include

from book import views as book_views


urlpatterns = [
    path('books/add/', book_views.AddBookView.as_view(), name="add book"),

    path('books/<int:pk>/', include([
        path('', book_views.BookDetailView.as_view(), name='book details'),
        path('edit/', book_views.BookUpdateView.as_view(), name='update book'),
        path('delete/', book_views.BookDeleteView.as_view(), name='delete book'),
    ]))
]