from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, AuthorSubscription, RoleRequest
from django.contrib.auth.models import User, Group
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


def has_written(author, post):
    return author in post.author.all()


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


def get_author_subscibers(user):
    if user.is_authenticated:
        return User.objects.filter(subscriber__author=user)
    else:
        return User.objects.none()


def get_category_subscriptions(user):
    if user.is_authenticated:
        return Category.objects.filter(subscribers=user)
    else:
        return Category.objects.none()


def is_author_already_subscribed_to_user(author, user):
    if user.is_authenticated:
        subscribed_users = get_author_subscriptions(user)
        for sub_user in subscribed_users:
            if sub_user == user:
                return True
    return False


def user_info(user):
    if user.is_authenticated:
        user_subscriptions = get_author_subscriptions(user).count()
        user_subscribers = get_author_subscibers(user).count()
        return user_subscriptions, user_subscribers


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
    return render(request, "view_content/index.html", {'posts': posts.order_by("-date")[:20]})


def create_content(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not is_author(request.user):
        return redirect("/")
    post = Post()
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            post.author.add(request.user)
            return redirect("/")
    else:
        form = AuthorForm(initial=post.__dict__)

    return render(request, "view_content/create.html", {'form': form})


def detail_post(request, post_id ):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_content/detailPost.html', {'post': post})


def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('/')
    post = get_object_or_404(Post, id=post_id)
    I_am_the_author = has_written(request.user, post)
    if request.method == 'POST':
        if is_executive_editor(request.user):
            form = ExEditorForm(request.POST, instance=post)
        elif post.editor == request.user and post.needs_proofreading:
            form = EditorForm(request.POST, instance=post)
        elif I_am_the_author:
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
        initial['author'] = [author.id for author in post.author.all()]
        if is_executive_editor(request.user):
            form = ExEditorForm(initial=initial)
        elif post.editor == request.user:
            form = EditorForm(initial=initial)
        elif I_am_the_author:
            form = AuthorForm(initial=initial)
        else:
            return redirect("/my_page/")

    return render(request, "view_content/edit.html", {'form': form, 'I_am_the_author': I_am_the_author, 'post': post})

def add_category(request):
	if request.method == 'POST': 
		get_text = str(request.POST.get('new_cat'))
		if Category.objects.filter(name=get_text):	
			return redirect('/')
		new_category = Category.objects.create(name=get_text)
	return redirect('/subscriptions/')


def my_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    I_am_editor = is_editor(request.user)
    posts = Post.objects.filter(author=request.user)
    needs_proofreading = Post.objects.filter(needs_proofreading=True)
    groups = Group.objects.all
    role_requests = RoleRequest.objects.all()
    return render(request, "view_content/my_page.html",
                  {'posts': posts, 'needs_proofreading': needs_proofreading, 'is_editor': I_am_editor, 'groups': groups, 'role_requests': role_requests})


def executive_page(request):
    if not is_executive_editor(request.user):
        return redirect("/")
    needs_approval = Post.objects.filter(needs_approval=True, published=False)
    published = Post.objects.filter(published=True)
    posts = Post.objects.all()
    other = Post.objects.all().difference(needs_approval).difference(published)

    editors = get_group_members('editor')
    selected_value = request.GET.get("selected_value")
    selected_post = request.GET.get("selected_post")
    if selected_value:
        post = Post.objects.get(id=selected_post)
        post.editor = User.objects.get(username=selected_value)
        post.save()
    return render(request, "view_content/executive_page.html", {'needs_approval': needs_approval,
                                                                'published': published,
                                                                'posts': posts,
                                                                'other': other,
                                                                'editors': editors
                                                                })


def assign_post_editor_to_logged_in_user(request, post_id):
    if not request.user.is_authenticated:
        return redirect('/')
    if is_editor(request.user):
        post = Post.objects.get(id=post_id)
        post.editor = request.user
        post.save()
    return redirect("/my_page/")


def delete_request(request, role_request_id):
    role_request = RoleRequest.objects.get(id=role_request_id)
    role_request.delete()
    return redirect('/my_page/')


def request_role(request, group_id):
    if not request.user.is_authenticated:
        return redirect('/')
    the_group = Group.objects.get(id=group_id)
    role_request = RoleRequest(group=the_group, user=request.user)
    role_request.save()
    return redirect("/my_page/")


def approve_user_group(request, role_request_id):
    if not request.user.is_authenticated and request.user.is_superuser:
        return redirect('/')
    role_request = RoleRequest.objects.get(id=role_request_id)
    the_group = role_request.group
    user_requesting_new_role = role_request.user
    the_group.user_set.add(user_requesting_new_role)
    if the_group.name == 'executive editor':
        the_group = Group.objects.get(name='editor')
        the_group.user_set.add(user_requesting_new_role)
    role_request.delete()
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


def unsubscribe_to_category(request, category_id):
	category = Category.objects.get(pk=category_id)
	category.subscribers.remove(request.user)
	return redirect("/subscriptions/")
	
def unsubscribe_to_author(request, author_id):
	author = User.objects.get(pk=author_id)
	if not request.user.is_authenticated:
		return redirect('/')
	author_subscription = AuthorSubscription.objects.filter(
										author=author,
										subscriber = request.user)
	author_subscription.first().delete()
	return redirect("/subscriptions/")



def confirm_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if has_written(request.user, post):
        return render(request, "view_content/confirm_delete.html", {'post': post})
    else:
        return redirect("/edit/"+post_id)


def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if has_written(request.user, post):
        post.delete()
    return redirect("/my_page/")


def submit_for_proofreading(request, post_id):
    post = Post.objects.get(id=post_id)
    if has_written(request.user, post):
        post.needs_proofreading = True
    post.save()
    return redirect("/my_page/")


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


def my_profile(request):
    if not request.user.is_authenticated:
        return redirect("/")
    user = request.user
    user_subscriptions, user_subscribers = user_info(user)
    return render(request, "view_content/my_profile.html", {'user': user, 'user_subscriptions': user_subscriptions,'user_subscribers': user_subscribers })


def show_users_profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect("/")
    user = User.objects.get(id=user_id)
    user_subscriptions, user_subscribers = user_info(user)
    author = is_author(user)
    already_subscribed = is_author_already_subscribed_to_user(user, request.user)
    return render(request, "view_content/show_user_profile.html", {'user': user, 'author': author, 'already_subscribed': already_subscribed, 'user_subscriptions': user_subscriptions,'user_subscribers': user_subscribers})

