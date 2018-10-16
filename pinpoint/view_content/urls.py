from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="home"),
    path('create/', views.create_content, name="content"),
    path('edit/<post_id>', views.edit_post, name="edit"),
    path('assign/<post_id>', views.assign_post_editor_to_logged_in_user),
    path('my_page/', views.my_page ,name ="my_page"),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscribe/<author_id>', views.subscribe_to_author),
    path('<post_id>', views.detailPost, name='detail'),
]
