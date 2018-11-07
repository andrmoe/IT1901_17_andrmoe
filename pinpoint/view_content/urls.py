from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('create/', views.create_content, name="content"),
    path('edit/<post_id>', views.edit_post, name="edit"),
    path('assign/<post_id>', views.assign_post_editor_to_logged_in_user),
    path('my_page/', views.my_page ,name ="my_page"),
    path('save_post/<post_id>', views.save_post_to_user),
    path('saved_posts/', views.view_saved_content, name="saved_posts"),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscribe_author/<author_id>', views.subscribe_to_author),
    path('subscribe_category/<category_id>', views.subscribe_to_category),
    path('request/role/<group_id>', views.request_role),
    path('approve/role/<role_request_id>', views.approve_user_group),
    path('deny/role/<role_request_id>', views.delete_request),
    path('<post_id>', views.detail_post, name='detail'),
    path('edit/<post_id>/confirm_delete/', views.confirm_delete, name='confirm_delete'),
    path('edit/<post_id>/delete/', views.delete_post, name='delete'),
    path('executive_page/', views.executive_page, name='executive_page'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('submit_to_proofreading/<post_id>', views.submit_for_proofreading),
    path('profile/<user_id>', views.show_users_profile, name='view_profile')
]
