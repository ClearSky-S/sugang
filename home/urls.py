from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 메인페이지, 로그인 X일 경우 로그인 페이지로 리다이렉트 됨

    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'), # 로그인
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/', views.home, name='user'),  # 사용자 정보 조회 및 수정

    path('lectures/', views.lectures, name='lectures'),  # 강의 목록 조회 및 수강신청
    path('lectures/<int:class_id>/', views.enroll, name='enroll'),  # 강의 정보 및 신청

    path('mylectures/', views.mylectures, name='mylectures'),  # 신청한 강의 확인
    path('timetable/', views.home, name='timetable'),  # 시간표 확인
    path('cancel/<int:class_id>/', views.cancel, name='cancel'),  # 강의 취소 post method 만 허용

    path('admin/statistics/', views.home, name='statistics'), # 분석 정보 제공
    path('admin/timetable/<int:student_id>/', views.home, name='admin/timetable'),  # 분석 정보 제공

]