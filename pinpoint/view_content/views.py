from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, AuthorSubscription
from django.contrib.auth.models import User
from .forms import AuthorForm, EditorForm


def is_editor(user):
    if user.is_authenticated:
        return user.groups.filter(name='editor').exists()
    else:
        return False


def is_author(user):
    if user.is_authenticated:
        return user.groups.filter(name='authors').exists()
    else: return False


def get_subscribed_content(user):
    if user.is_authenticated:
        return (Post.objects.filter(author__subscriber__subscriber=user) |
                Post.objects.filter(categories__subscribers=user)).distinct().order_by('-date')
    else:
        return Post.objects.none()


def get_author_subscriptions(user):
    if user.is_authenticated:
        return User.objects.filter(subscriber__subscriber=user)
    else:
        return User.objects.none()


def get_category_subscriptions(user):
    if user.is_authenticated:
        return Category.objects.filter(subscribers=user)
    else:
        return Category.objects.none()


def index(request):
    posts = Post.objects.all().order_by("-date")[:20]
    return render(request, "view_content/TEMPORARY.html", {'posts': posts})


def create_content(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not is_author(request.user):
        return redirect("/")
    post = Post(author=request.user)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = AuthorForm(initial=post.__dict__)

    return render(request, "view_content/create.html", {'form': form})


def detailPost(request, post_id ):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_content/detailPost.html', {'post': post})


def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('/')
    post = get_object_or_404(Post, id=post_id)
    I_am_the_author = post.author == request.user
    if request.method == 'POST':
        if post.editor == request.user:
            form = EditorForm(request.POST, instance=post)
        elif post.author == request.user:
            form = AuthorForm(request.POST, instance=post)
        else:
            return redirect("/my_page/")
        if form.is_valid():
            form.save()
            return redirect("/my_page/")
    else:
        if post.editor == request.user:
            form = EditorForm(initial=post.__dict__)
        elif post.author == request.user:
            form = AuthorForm(initial=post.__dict__)
        else:
            return redirect("/my_page/")

    return render(request, "view_content/edit.html", {'form': form, 'I_am_the_author': I_am_the_author, 'post': post})


def my_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    I_am_editor = is_editor(request.user)
    subscribed_content = get_subscribed_content(request.user)
    subscriptions = get_author_subscriptions(request.user)
    subscriptions_cat = get_category_subscriptions(request.user)
    posts = Post.objects.filter(author=request.user)
    needs_proofreading = Post.objects.filter(needs_proofreading=True)
    return render(request, "view_content/my_page.html",
                  {'posts': posts, 'needs_proofreading': needs_proofreading, 'subscribed_content': subscribed_content,
                   'subscriptions': subscriptions, 'subscriptions_cat': subscriptions_cat, 'is_editor': I_am_editor})


def assign_post_editor_to_logged_in_user(request, post_id):
    if not request.user.is_authenticated:
        return redirect('/')
    if is_editor(request.user):
        post = Post.objects.get(id=post_id)
        post.editor = request.user
        post.save()
    return redirect("/my_page/")


def subscribe_to_author(request, author_id):
    if not request.user.is_authenticated:
        return redirect('/')
    author = User.objects.get(pk=author_id)
    if is_author(author):
        subscription = AuthorSubscription(subscriber=request.user, author=author)
        subscription.save()
    return redirect("/subscriptions/")


def subscriptions(request):
    print(request.user)
    if not request.user.is_authenticated:
        return redirect('/')
    subscribed_content = get_subscribed_content(request.user)
    subscriptions = get_author_subscriptions(request.user)
    subscriptions_cat = get_category_subscriptions(request.user)
    return render(request, "view_content/subscriptions.html", {'subscribed_content': subscribed_content,
                   'subscriptions': subscriptions, 'subscriptions_cat': subscriptions_cat})
