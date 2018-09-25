from django.urls import path
from . import views


urlpatterns = [
    # register
    path('', views.register, name="register"),
    path('welcome/', views.welcome, name="home")
]
