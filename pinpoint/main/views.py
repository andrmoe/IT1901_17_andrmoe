from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('welcome/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def welcome(request):
    return HttpResponse("<h1>Hey " + request.user.username + "!</h1>")