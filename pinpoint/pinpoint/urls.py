from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('view_content/', include('view_content.urls')),
    path('admin/', admin.site.urls),
]
