from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="home"),
    path('create/', views.create_content, name="content"),
    path('<post_id>', views.detailPost, name='detail'),

]
