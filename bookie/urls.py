
from django.urls import path

from bookie import views as bookie_views


urlpatterns = [
    path('register/', bookie_views.RegisterBookieView.as_view(), name='register bookie'),
    path('login/', bookie_views.BookieLoginView.as_view(), name='login bookie'),
    path('logout/', bookie_views.logout_view, name="logout bookie"),
    path('<int:pk>/', bookie_views.ProfileDetailView.as_view(), name='bookie profile'),
    path('<int:pk>/edit/', bookie_views.ProfileUpdateView.as_view(), name='edit bookie profile'),
    path('<int:pk>/delete/', bookie_views.ProfileDeleteView.as_view(), name='delete bookie profile'),
]


"""
superuser:
        denny
        denny
        
        
staff:
    yoda
    yoda11
    age: 35
"""