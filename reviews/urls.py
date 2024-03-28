
from django.urls import path
from reviews import views

urlpatterns = [
    path('sumbit_review/<int:book_id>', views.submit_review, name='submit review'),
    path('delete_review/<int:book_id>', views.DeleteReview.as_view(), name='delete review'),
]