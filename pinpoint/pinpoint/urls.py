from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', include('view_content.urls')),
    path('accounts/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls'))
]
