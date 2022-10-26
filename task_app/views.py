from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core import validators
from django.core.serializers import serialize
from django.forms import URLField
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Urls
from base_user.models import MyUser
from base_user.forms import MyUserCreationForm, LoginForm
from urllib.parse import urlparse
from urllib.request import urlopen


def home(request):
    context = {}
    context['urls'] = Urls.objects.all()
    return render(request, 'home.html', context)


# Create your views here.
def register(request):
    context = {}
    context['form'] = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('login_user')
        else:
            messages.error(request, form.errors)
            return redirect('register_user')
    return render(request, 'signup.html', context)


def login_user(request):
    context = {}
    context['form'] = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, form.errors)
                return redirect('login_user')
    return render(request, 'login.html', context)


def check_url(request):
    urls = Urls.objects.all()
    url_list = []
    for e in urls:
        result = {
            'id': e.id,
            'url': e.url,
            'user': e.user.username,
            'status': e.status
        }
        url_list.append(result)

    return JsonResponse(url_list, safe=False)
