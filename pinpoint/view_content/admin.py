from django.contrib import admin
from .models import Post, AuthorSubscription, Category, RoleRequest

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(AuthorSubscription)
admin.site.register(RoleRequest)
