from django.urls import path
from . import views
from django.views.generic.list import ListView


urlpatterns = [
    path('', views.index, name="home"),
    path('create/', views.create_content),
]
