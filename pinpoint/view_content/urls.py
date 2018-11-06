from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="home"),
    path('create/', views.create_content, name="content"),
    path('edit/<post_id>', views.edit_post, name="edit"),
    path('assign/<post_id>', views.assign_post_editor_to_logged_in_user),
    path('my_page/', views.my_page ,name ="my_page"),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscribe_author/<author_id>', views.subscribe_to_author),
    path('subscribe_category/<category_id>', views.subscribe_to_category),
    path('request/role/<group_id>', views.request_role),
    path('approve/role/<role_request_id>', views.approve_user_group),
    path('deny/role/<role_request_id>', views.delete_request),
    path('<post_id>', views.detailPost, name='detail'),
]
