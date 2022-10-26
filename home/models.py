from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.template.defaultfilters import default

# 티어가 낮은 모델은 더 높은 티어의 모델에 의존적이다.
# 즉, DB 삽입 명령을 수행할 때 높은 티어부터 실행해야한다.
# Tier 1 Model: 전공, 건물, 과목
# Tier 2 Model: 교강사, 강의실
# Tier 3 Model: 학생, 수업
# Tier 4 Model: 성적, 수업시간, +auth_user




# ----------- Tier 1 ---------------
# Tier 1 Model: 전공, 건물, 과목

class Major(models.Model):
    """
    major_id,name
    1,건설환경공학과
    """
    major_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Building(models.Model):
    """
    building_id,name,admin,rooms
    305,IT / BT,공과대학,19
    """
    building_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    admin = models.CharField(max_length=100)
    rooms = models.IntegerField()
    def __str__(self):
        return self.name


class Course(models.Model):
    """
    course_id,name,credit
    CIE3022,철근콘크리트구조설계,3
    """
    course_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    credit = models.IntegerField()
    def __str__(self):
        return self.name


# ----------- Tier 2 ---------------
# Tier 2 Model: 교강사, 강의실

class Lecturer(models.Model):
    """
    lecturer_id,name,major_id
    2001001001,조병완,1
    """
    lecturer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Room(models.Model):
    """
    room_id,building_id,occupancy
    1,305,140
    """
    room_id = models.IntegerField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    occupancy = models.IntegerField()
    def __str__(self):
        return str(self.building) + str(self.room_id)
# ----------- Tier 3 ---------------
# Tier 3 Model: 학생, 수업

class Student(models.Model):
    # csv 라이브러리로 파싱 후 수동 셋업 필요
    """
    student_id,password,name,sex,major_id,lecturer_id,year
    2018003125,125125125,정남아,female,44,2001032011,4
    """
    student_id = models.IntegerField(primary_key=True)
    # password : 보안상 auth_user 테이블로 분리함
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=20)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    year = models.IntegerField()
    state = models.CharField(max_length=20, default="재학")

    def __str__(self):
        return self.name + " / " + str(self.student_id)

class Class(models.Model):
    """
    class_id,class_no,course_id,(name),(major_id),year,(credit),lecturer_id,person_max,opened,room_id
    8831,10003,CIE3022,철근콘크리트구조설계,1,1,3,2001001001,3,2022,169
    """
    class_id = models.IntegerField(primary_key=True)
    class_no = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100) : DB 스키마에서 삭제 가능 Course에 이미 있음

    # major_id: # FK, DB 스키마에서 화살표 빠진거 보충 필요
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    year = models.IntegerField()
    # credit = models.IntegerField() :  DB 스키마에서 삭제 가능 Course에 이미 있음
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    person_max = models.IntegerField()
    opened = models.IntegerField()
    enrolled = models.ManyToManyField(Student, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.course) + " / " + str(self.lecturer)
    def clean(self):
        if self.person_max > self.room.occupancy:
            raise ValidationError("수강 정원이 강의실의 최대 수용인원보다 많습니다.")

# ----------- Tier 4 ---------------
# Tier 4 Model: 성적, 수업시간, +auth_user(장고 기본 auth DB 이용)

class Credits(models.Model):
    """
    credits_id,student_id,course_id,year,grade
    1,2018003125,GEN5026,2022,B0
    """
    credits_id = models.IntegerField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    grade = models.CharField(max_length=2)


class Time(models.Model):
    # csv 라이브러리로 파싱 후 수동 셋업 필요
    """
    csv:
    time_id,class_id,period,begin,end
    1,8831,1,1900-01-02T05:30:00.000Z,1900-01-02T07:00:00.000Z
    """
    """
    DB:
    time_id,class_id,period,day,begin,end
    1,8831,1,5,05:30,05:30
    """
    time_id = models.IntegerField(primary_key=True)
    classInfo = models.ForeignKey(Class, on_delete=models.CASCADE)  # class 는 예약어여서 사용할 수 없음
    period = models.IntegerField()
    # begin = models.DateTimeField() 스키마 수정 필요
    # end = models.DateTimeField() 스키마 수정 필요
    day = models.IntegerField(null=True, blank=True)
    begin = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

class User(AbstractUser):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)


class WishClass(models.Model):
    classInfo = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
