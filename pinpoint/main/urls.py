from django.urls import path, include
from . import views


urlpatterns = [
    path('register/welcome/', views.welcome, name="welcome"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('', include('django.contrib.auth.urls')),
    path('my_profile/edit/', views.edit_profile, name='edit_profile'),
    path('my_profile/change_password/', views.change_password, name='change_passoword')
]
