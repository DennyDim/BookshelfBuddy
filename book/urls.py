
from django.urls import path, include

from book import views as book_views


urlpatterns = [

    path('search/', book_views.search_view , name='search by title'),

    path('add-to-wishlist/', book_views.AddBookToWishlistView.as_view(), name='add to wishlist'),
    path('already-read/', book_views.AddBookToAlreadyReadView.as_view(), name='add to already read'),
    path('random/', book_views.generate_random_book, name='generate random book'),

    path('books/add/', book_views.AddBookView.as_view(), name="add book"),



    path('books/<int:pk>/', include([
        path('', book_views.BookDetailView.as_view(), name='book details'),
        path('edit/', book_views.BookUpdateView.as_view(), name='update book'),
        path('delete/', book_views.BookDeleteView.as_view(), name='delete book'),

    ]))

]
