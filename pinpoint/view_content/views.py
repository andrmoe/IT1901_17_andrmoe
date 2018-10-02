from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm


def index(request):
    posts = Post.objects.all().order_by("-date")[:20]
    return render(request, "view_content/TEMPORARY.html", {'posts': posts})


def create_content(request):
    post = Post.objects.get(pk=2)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = PostForm(initial=post.__dict__)

    return render(request, "view_content/create.html", {'form': form})

def detailPost(request, post_id ):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_content/detailPost.html', {'post':post})
