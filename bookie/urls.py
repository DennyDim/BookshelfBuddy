
from django.urls import path

from bookie import views as bookie_views


urlpatterns = [
    path('register/', bookie_views.RegisterBookieView.as_view(), name='register bookie'),
    path('login/', bookie_views.BookieLoginView.as_view(), name='login bookie'),
    path('logout/', bookie_views.BookieLogoutView.as_view(), name="logout bookie"),
    path('<int:pk>', bookie_views.BookieProfile.as_view(), name='bookie profile'),
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