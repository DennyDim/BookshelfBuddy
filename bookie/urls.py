
from django.urls import path, include

from bookie import views as bookie_views


urlpatterns = [

    path('register/', bookie_views.RegisterBookieView.as_view(), name='register bookie'),

    path('login/', bookie_views.BookieLoginView.as_view(), name='login bookie'),
    path('logout/', bookie_views.logout_view, name="logout bookie"),

    path('<int:pk>/profile/', include([

        path('', bookie_views.ProfileDetailView.as_view(), name='bookie profile'),
        path('edit/', bookie_views.ProfileUpdateView.as_view(), name='edit bookie profile'),
        path('delete/', bookie_views.my_delete, name='delete bookie profile'),
    ])),
]
