
from django.urls import path, include

from author import views as author_views


urlpatterns = [

    path('all_writers/', author_views.AuthorsListView.as_view(), name='all_writers'),
    path('all_writers/<int:page>/', author_views.AuthorsListView.as_view(), name='all_writers_paginated'),

    path('add_author/', author_views.AddAuthorView.as_view(), name='create new author'),

    path('<int:pk>/', include([

        path('edit_author/', author_views.AuthorUpdateView.as_view(), name='edit author'),
        path('author_detail/', author_views.AuthorDetailView.as_view(), name='author details'),

        path('delete_author/', author_views.AuthorDeleteView.as_view(), name='delete author'),
        path('like/', author_views.like_author, name='like author'),
    ]))
]
