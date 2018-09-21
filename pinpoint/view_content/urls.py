from django.urls import path
from . import views
from django.views.generic.list import ListView
from .models import Post


urlpatterns = [
    path('', ListView.as_view(queryset=Post.objects.all().order_by("-date")[:20],
                              template_name="view_content/TEMPORARY.html"), name="index")
]
