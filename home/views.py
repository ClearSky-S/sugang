from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q

# 숫자를 요일로 바꿔주는 함수
def numberToWeekday(num):
    weekdayDict = {
        1: "월",
        2: "화",
        3: "수",
        4: "목",
        5: "금",
        6: "토",
    }
    return weekdayDict[num]+"요일"


# 메인페이지, 수강신청 관련 공지를 보여줌
def home(request):
    if request.user.is_superuser:
        return redirect('/admin')
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    context = {

    }
    return render(request, 'home/home.html', context)

# 강의 목록을 보여줌
def lectures(request):
    if request.user.is_superuser:
        return redirect('/admin')
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    kw = request.GET.get('kw', '')  # 검색어
    page = request.GET.get('page', '1')  # 페이지
    classInfoList = Class.objects.filter(opened=2022).order_by('class_id')
    if(kw):
        try:
            int(kw)
            classInfoList = classInfoList.filter(
                Q(class_id=kw) |
                Q(course=kw) |
                Q(course__name__icontains=kw) |
                Q(lecturer__name=kw)

            ).distinct()
        except:
            classInfoList = classInfoList.filter(
                Q(course=kw) |
                Q(course__name__icontains=kw) |
                Q(lecturer__name=kw)
            ).distinct()


    paginator = Paginator(classInfoList, 30)  # 페이지당 30개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {
        "classInfoList": page_obj,
        "kw": kw,
        "page": page,
    }
    return render(request, 'home/lectures.html', context)


# GET 요청 시 강의 정보를 보여줌
# POST 요청 시 validation 후 강의를 신청함
def enroll(request, class_id):
    if request.user.is_superuser:
        return redirect('/admin')
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    classInfo = get_object_or_404(Class, pk=class_id)
    try:
        isEnrolled = classInfo.enrolled.filter(student_id=request.user.student.student_id)[0]
        isEnrolled = True
    except:
        isEnrolled = False
    errorMessage = ""
    if request.method == 'POST':

        # B0 가 넘는지 확인
        isOverB0 = False
        credits = Credits.objects.filter(student=request.user.student, course=classInfo.course)
        for credit in credits:
            if credit.grade=="B0":
                isOverB0 = True
                break
            if credit.grade=="B+":
                isOverB0 = True
                break
            if credit.grade=="A0":
                isOverB0 = True
                break
            if credit.grade=="A+":
                isOverB0 = True
                break
        isMaxPerson = classInfo.enrolled.count() >= classInfo.person_max

        isSameTime = False

        isOverMaxCredit = False
        if isEnrolled:
            errorMessage = "이미 신청한 강의입니다."
        elif isOverB0:
            errorMessage = "이전 성적이 B0 이상으로 신청할 수 없습니다."
        elif isMaxPerson:
            errorMessage = "정원이 가득 찼습니다."
        elif isSameTime:
            # 해야 함
            errorMessage = "이미 같은 시간대의 다른 강의가 있습니다."
        elif isOverMaxCredit:
            # 해야 함
            errorMessage = "최대 학점 제한인 18학점을 초과했습니다."
        else:
            classInfo.enrolled.add(request.user.student)
            return redirect(reverse('mylectures'))

    timeList = []
    for element in classInfo.time_set.all():
        d = dict()
        d["day"] = numberToWeekday(element.day)
        d["begin"] = element.begin
        d["end"] = element.end
        timeList.append(d)
    context = {
        "classInfo": classInfo,
        "timeList": timeList,
        "errorMessage": errorMessage,
        "isEnrolled":isEnrolled,
    }
    return render(request, 'home/lectureDetail.html', context)


# 강의 취소 POST 요청
def cancel(request, class_id):
    classInfo = get_object_or_404(Class, pk=class_id)
    try:
        enrolled = classInfo.enrolled.filter(student_id=request.user.student.student_id)[0]
    except:
        return redirect(reverse('mylectures'))

    classInfo.enrolled.remove(enrolled)
    return redirect(reverse('mylectures'))

def mylectures(request):
    classInfoList = Class.objects.filter(enrolled=request.user.student).order_by('class_id')
    context = {
        "classInfoList": classInfoList,

    }
    return render(request, 'home/mylectures.html', context)