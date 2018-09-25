from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def index(request):
    posts = Post.objects.all().order_by("-date")[:20]
    return render(request, "view_content/TEMPORARY.html", {'posts': posts})


def create_content(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, "view_content/create.html", {'form': form})

