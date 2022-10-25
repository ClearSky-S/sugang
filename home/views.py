from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from django.core.paginator import Paginator


def home(request):
    if request.user.is_superuser:
        return redirect('/admin')
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    context = {

    }
    return render(request, 'home/home.html', context)


def lectures(request):
    # 할 일: 검색 필터 기능 추가
    # a = Student.objects.all()[0]
    # print(a)
    # b = a.class_set.all()
    # print(b)
    if request.user.is_superuser:
        return redirect('/admin')
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    page = request.GET.get('page', '1')  # 페이지
    classInfoList = Class.objects.all()
    paginator = Paginator(classInfoList, 30)  # 페이지당 30개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {
        "classInfoList": page_obj
    }
    return render(request, 'home/lectures.html', context)


def lectureDetail(request, lecture_id):
    # 할 일: 강의 상세 정보 보기, 강의 신청 버튼
    if request.user.is_superuser:
        return redirect('/admin')
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    classInfo = get_object_or_404(Class, pk=lecture_id)
    # classInfo = Student.objects.get(pk=request.user.student_id).class_set.get(pk=lecture_id)
    context = {
        "classInfo": classInfo
    }
    return render(request, 'home/lectureDetail.html', context)
