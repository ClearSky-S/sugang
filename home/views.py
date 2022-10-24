from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import *


def home(request):
    if request.user.is_superuser:
        return redirect('/admin')

    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    context = {
        "classInfoList": Class.objects.all()
    }
    return render(request, 'home/home.html', context)

def login(request):
    context = {
        "classInfoList": Class.objects.all()
    }
    return render(request, 'home/home.html', context)