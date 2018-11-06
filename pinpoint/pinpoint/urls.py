from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('accounts/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('', include('view_content.urls')),
]
