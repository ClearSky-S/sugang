from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.timezone import now, localtime
from datetime import datetime

# 숫자를 요일로 바꿔주는 함수
def numberToWeekday(num):
    if num==None:
        return "X"
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
        enrolledClassList = classInfo.enrolled.filter(student_id=request.user.student.student_id)
        enrolledClassList[0]
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

        # 시간 겹치는 지 확인
        enrolledClassList = Class.objects.filter(enrolled__student_id=request.user.student.student_id)
        isSameTime = False
        for time1 in classInfo.time_set.all():
            if not time1.begin: continue
            for c in enrolledClassList:
                for time2 in c.time_set.all():
                    if not time2.begin: continue
                    if time1.day==6 or time2.day==6:
                        continue
                    if time1.begin >= datetime(1,1,1,18,0).time() or time2.begin >= datetime(1,1,1,18,0).time():
                        continue
                    if time1.day != time2.day:
                        continue
                    if time1.begin <= time2.begin and time2.begin < time1.end:
                        isSameTime = True
                        break
                    if time2.begin <= time1.begin and time1.begin < time2.end:
                        isSameTime = True
                        break
                if isSameTime: break
            if isSameTime: break

        isOverMaxCredit = False
        sumCredit = 0

        # 총 학점 18학점 이하인지 확인
        for classInfo2 in enrolledClassList:
            sumCredit += classInfo2.course.credit
        sumCredit += classInfo.course.credit
        print(sumCredit)
        if sumCredit >= 18:
            isOverMaxCredit = True

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
    isWishClass = WishClass.objects.filter(classInfo__class_id=class_id, student = request.user.student)
    context = {
        "classInfo": classInfo,
        "timeList": timeList,
        "errorMessage": errorMessage,
        "isEnrolled": isEnrolled,
        "isWishClass": isWishClass,
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
        "title": "신청 목록",
        "classInfoList": classInfoList,

    }
    return render(request, 'home/mylectures.html', context)



def wishlist(request):
    classInfoList = []
    for wishClass in WishClass.objects.filter(student=request.user.student):
        classInfoList.append(wishClass.classInfo)
    context = {
        "title":"희망목록",
        "classInfoList": classInfoList,

    }
    return render(request, 'home/mylectures.html', context)
def wishEnroll(request, class_id):
    if request.method=="POST":
        wishClassList = WishClass.objects.filter(classInfo__class_id=class_id, student=request.user.student)
        if wishClassList:
            wishClassList.delete()
            return redirect(reverse('wishlist'))
        wishClass = WishClass()
        wishClass.student = request.user.student
        wishClass.classInfo = Class.objects.get(pk=class_id)
        wishClass.save()
    return redirect(reverse('wishlist'))

gradeDict={
    "A+": 4.5,
    "A0": 4.0,
    "A+": 3.5,
    "B+": 3.0,
    "B0": 2.5,
    "C+": 2.0,
    "C0": 1.5,
    "D+": 1.0,
    "D0": 0.5,
    "F": 0,
}

def statistics(request):
    if not request.user.is_superuser:
        return redirect(reverse("home"))
    courseList = Course.objects.all()
    courseList2 = []
    s=0
    for course in courseList:
        if course.credits_set.count() == 0:
            continue
        element = {"course":course}
        creditsList = [gradeDict[e.grade] for e in course.credits_set.all()]
        avg = sum(creditsList)/len(creditsList)
        s += avg
        element["avgGrade"] = round(avg,2)
        courseList2.append(element)
    courseList2= sorted(courseList2, key=lambda c: c["avgGrade"])
    total_avg = s/len(courseList2)
    for c in courseList2:
        c["diff"] = round(total_avg-c["avgGrade"],2)

    context = {
        "courseList": courseList2[0:10],
        "total_avg": total_avg,
    }
    return render(request, 'home/statistics.html', context)

def timetable(request, student_id = None):
    if not request.user.is_superuser:
        student_id = request.user.student.student_id
    timetableList = Time.objects.filter(classInfo__enrolled__student_id=student_id)
    timetableList2 = [[] for i in range(0,6)]
    for element in timetableList:
        timetableList2[element.day].append(element)
    for day in timetableList2:
        day.sort(key= lambda x: x.begin)
    timetableList3 = []
    for day in timetableList2:
        for element in day:
            d = {
                "day": numberToWeekday(element.day),
                "time": element
            }
            timetableList3.append(d)


    context={
        "timetableList": timetableList3
    }
    return render(request, 'home/timetable.html', context)
