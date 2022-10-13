from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 메인페이지, 로그인 X일 경우 로그인 페이지로 리다이렉트 됨

    path('login/', views.home, name='login'), # 로그인
    path('user/', views.home, name='user'),  # 사용자 정보 조회 및 수정

    path('lectures/', views.home, name='lectures'),  # 강의 목록 조회 및 수강신청
    path('enroll/<int:lecture_id>/', views.home, name='enroll'),  # 강의 수강 신청 Post method 만 허용
    path('mylectures/', views.home, name='mylectures'),  # 신청한 강의 확인
    path('timetable/', views.home, name='timetable'),  # 시간표 확인
    path('cancel/<int:lecture_id>/', views.home, name='cancel'),  # 강의 취소 post method 만 허용

    path('statistics', views.home, name='statistics'), # 분석 정보 제공

    path('chat', views.home, name='chat'),  # 추가기능: AJAX를 통한 실시간 채팅 기능



]