
from django.urls import path
from reviews import views



urlpatterns = [
    path('submit_review/<int:book_id>', views.submit_review, name='submit review'),
    path('delete_review/<int:pk>', views.DeleteReview.as_view(), name='delete review'),
]