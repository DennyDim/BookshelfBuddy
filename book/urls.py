
from django.urls import path, include

from book import views as book_views


urlpatterns = [

    path('paginated_books/<int:page>/', book_views.BooksListView.as_view(), name='paginated books'),

    path('add-to-wishlist/', book_views.AddBookToWishlistView.as_view(), name='add to wishlist'),
    path('already-read/', book_views.AddBookToAlreadyReadView.as_view(), name='add to already read'),

    path('books/add/', book_views.AddBookView.as_view(), name="add book"),
    path('request-a-book/', book_views.BookRequestView.as_view(), name="request a book"),


    path('books/<int:pk>/', include([
        path('', book_views.BookDetailView.as_view(), name='book details'),
        path('edit/', book_views.BookUpdateView.as_view(), name='update book'),
        path('delete/', book_views.BookDeleteView.as_view(), name='delete book'),

    ]))

]
