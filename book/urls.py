
from django.urls import path, include

from book import views as book_views


urlpatterns = [
    path('books/<int:pk>/', include([
        path('', book_views.BookDetailView.as_view(), name='book_detail'),
    ]))
]