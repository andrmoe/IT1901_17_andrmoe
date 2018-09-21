from django.urls import path, include
from django.contrib import admin



urlpatterns = [
    path('', include('view_content.urls')),
    path('accounts/profile/', include('view_content.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
