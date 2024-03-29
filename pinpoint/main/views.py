from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, UserEditForm


def register(request):
    """Shows a register form."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('welcome/')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    """Logs the user out. Redirects to /accounts/login"""
    logout(request)
    return redirect('/accounts/login')


def welcome(request):
    """Redirects to /accounts/profile"""
    return redirect("/accounts/profile")


def profile(request):
    """Redirects to / (index)"""
    return redirect("/")


def edit_profile(request):
    """Lets user change their personal information."""
    initial = request.user.__dict__
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect("/my_profile/")
    else:
        form = UserEditForm(instance=user)
        return render(request, "view_content/edit_profile.html", {'form': form, 'user': user})
    

def change_password(request):
    """Lets the user change their password"""
    initial = request.user.__dict__
    if request.method == 'POST':
        form = SetPasswordForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("/my_profile/")
    else:
        form = SetPasswordForm(request.user)
        return render(request, "view_content/edit_profile.html", {'form': form})
