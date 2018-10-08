from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, EditForm
from django.contrib.auth.models import Group


def is_editor(user):
    return user.groups.filter(name='editor').exists()


def index(request):
    posts = Post.objects.all().order_by("-date")[:20]
    return render(request, "view_content/TEMPORARY.html", {'posts': posts})


def create_content(request):
    post = Post(author=request.user)
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


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and post.editor != request.user:
        return redirect("/my_page/")
    if request.method == 'POST':
        form = EditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("/my_page/")
    else:
        form = EditForm(initial=post.__dict__)

    return render(request, "view_content/edit.html", {'form': form, 'author': post.author})


def my_page(request):
    I_am_editor = is_editor(request.user)
    posts = Post.objects.filter(author=request.user)
    needs_proofreading = Post.objects.filter(needs_proofreading=True)
    return render(request, "view_content/my_page.html",
                  {'posts': posts, 'needs_proofreading': needs_proofreading, 'is_editor': I_am_editor})


def assign_post_editor_to_logged_in_user(request, post_id):
    if is_editor(request.user):
        post = Post.objects.get(id=post_id)
        post.editor = request.user
        post.save()
    return redirect("/my_page/")
