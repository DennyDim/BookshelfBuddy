
from django.urls import path, include

from bookie import views as bookie_views
from book import views as book_views


urlpatterns = (
    path('my-request/', book_views.user_requests, name='all bookies requests'),
    path('register/', bookie_views.RegisterBookieView.as_view(), name='register bookie'),
    path('login/', bookie_views.BookieLoginView.as_view(), name='login bookie'),
    path('logout/', bookie_views.logout_view, name="logout bookie"),

    path('<int:pk>/', include([
        path('', bookie_views.ProfileDetailView.as_view(), name='bookie profile'),
        path('edit/', bookie_views.ProfileUpdateView.as_view(), name='edit bookie profile'),
        path('delete/', bookie_views.delete_bookie, name='delete bookie profile'),

    ])
    ))

