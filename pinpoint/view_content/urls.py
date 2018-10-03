from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="home"),
    path('create/', views.create_content, name="content"),
    path('edit/<post_id>', views.edit_post, name="edit"),
    path('my_page/', views.my_page ,name ="my_page"),
    path('<post_id>', views.detailPost, name='detail'),

]
