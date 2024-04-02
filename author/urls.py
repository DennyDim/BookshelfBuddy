
from django.urls import path, include

from author import views as author_views


urlpatterns = [
    path('all_writers/', author_views.AuthorsListView.as_view(), name='all_writers'),
]
