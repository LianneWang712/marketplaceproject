from django.shortcuts import render
from account.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from product.models import Cart
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Create your views here.
def signup(request):
    context = {}
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                cart = Cart.objects.create(user=user)
                return HttpResponseRedirect(reverse('login'))
            except IntegrityError:
                form.add_error('username', 'This username is already taken')
        context['form'] = form
    return render(request, 'account/signup.html', context)


def do_login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is None:
                form.add_error(None, 'Wrong username or password')
            else:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('index'))
        context['form'] = form
    return render(request, 'account/login.html', context)


def do_logout(request):
    if request.user.is_authenticated:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {
            'type': 'logout_message',
            'message': 'Disconnecting. You logged out from another browser or tab.'})

    logout(request)
    return HttpResponseRedirect(reverse('index'))
