from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def home(request):
    context = {"classInfoList": Class.objects.all() }
    return render(request, 'home/home.html', context)
