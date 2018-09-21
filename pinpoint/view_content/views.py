from django.shortcuts import render
from .models import Post


def index(request):
    posts = Post.objects.all().order_by("-date")[:20]
    return render(request, "view_content/TEMPORARY.html", {'posts': posts, 'user': request.user})
