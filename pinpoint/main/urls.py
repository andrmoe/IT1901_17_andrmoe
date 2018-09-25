from django.urls import path, include
from . import views


urlpatterns = [
    # register
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('', include('django.contrib.auth.urls')),
]
