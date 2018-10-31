from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, AuthorSubscription
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import AuthorForm, EditorForm, ExEditorForm


def is_executive_editor(user):
    if user.is_authenticated:
        return user.groups.filter(name='executive editor').exists()
    else:
        return False

def is_editor(user):
    if user.is_authenticated:
        return user.groups.filter(name='editor').exists()
    else:
        return False


def is_author(user):
    if user.is_authenticated:
        return user.groups.filter(name='authors').exists()
    else: return False

def is_executive_editor(user):
    if user.is_authenticated:
        return user.groups.filter(name='executive editor').exists()
    else: return False


def get_group_members(group_name):
    return User.objects.filter(groups__name=group_name)


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
    posts = Post.objects.all()
    query = request.GET.get("q")
    if query:
        posts = posts.filter(
                            Q(title__contains=query) |
                            Q(body__contains=query) |
                            Q(author__username__contains=query) |
                            Q(categories__name__contains=query)
                            ).distinct()
    return render(request, "view_content/TEMPORARY.html", {'posts': posts.order_by("-date")[:20]})


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
        if  is_executive_editor(request.user):
            form = ExEditorForm(request.POST, instance=post)
        elif post.editor == request.user:
            form = EditorForm(request.POST, instance=post)
        elif post.author == request.user:
            form = AuthorForm(request.POST, instance=post)
        else:
            return redirect("/my_page/")
        if form.is_valid():
            form.save()
            if is_executive_editor(request.user):
                return redirect("/executive_page/")
            else:
                return redirect("/my_page/")
    else:
        initial = post.__dict__
        initial['categories'] = [category.id for category in post.categories.all()]
        if is_executive_editor(request.user):
            form = ExEditorForm(initial=initial)
        elif post.editor == request.user:
            form = EditorForm(initial=initial)
        elif post.author == request.user:
            form = AuthorForm(initial=initial)
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

def executive_page(request):
    if not is_executive_editor(request.user):
        return redirect("/")
    needs_approval = Post.objects.filter(needs_approval=True)
    published = Post.objects.filter(published=True)
    return render(request, "view_content/executive_page.html",{'needs_approval': needs_approval, 'published': published})


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


def subscribe_to_category(request, category_id):
    if not request.user.is_authenticated:
        return redirect('/')
    category = Category.objects.get(pk=category_id)
    category.subscribers.add(request.user)
    return redirect("/subscriptions/")


def subscriptions(request):
    if not request.user.is_authenticated:
        return redirect('/')
    subscribed_content = get_subscribed_content(request.user)
    subscriptions = get_author_subscriptions(request.user)
    subscriptions_cat = get_category_subscriptions(request.user)
    not_subscribed_authors = get_group_members("authors").difference(subscriptions)
    not_subscribed_categories = Category.objects.all().difference(subscriptions_cat)
    return render(request, "view_content/subscriptions.html", {'subscribed_content': subscribed_content,
                                                               'subscriptions': subscriptions,
                                                               'subscriptions_cat': subscriptions_cat,
                                                               'not_subscribed_authors': not_subscribed_authors,
                                                               'not_subscribed_categories': not_subscribed_categories})

def confirm_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.author:
        return render(request, "view_content/confirm_delete.html", {'post': post})


def delete_post(post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.author:
        post.delete()
        return render(request, "view_content/my_page.html", {'post': post})

def save_post_to_user(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user.is_authenticated:
        post.saved_users.add(request.user)
    return redirect("/"+post_id)

def get_saved_content(user):
        return Post.objects.filter(saved_users=user).order_by('-date')

def view_saved_content(request):
    if not request.user.is_authenticated:
        return redirect("/")
    return render(request, "view_content/saved_posts.html", {'saved_posts': get_saved_content(request.user)})
