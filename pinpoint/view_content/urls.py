from django.urls import path
from . import views
from django.views.generic.list import ListView


urlpatterns = [
    path('', views.index),

]
