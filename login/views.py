# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import auth


# Create your views here.
def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('main')
        else:
            context = {'login_error': 'Пользователь не найден'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')
