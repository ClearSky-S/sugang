from django.db import models

# Create your models here.
from django.template.defaultfilters import default

# 티어가 낮은 모델은 더 높은 티어의 모델에 의존적이다.
# 즉, DB 삽입 명령을 수행할 때 높은 티어부터 실행해야한다.
# Tier 1 Model: 전공, 건물, 과목
# Tier 2 Model: 교강사, 강의실
# Tier 3 Model: 학생, 수업
# Tier 4 Model: 성적, 수업시간, +auth_user

# ----------- Tier 1 ---------------

class Major(models.Model):
    """
    major_id,name
    1,건설환경공학과
    """
    major_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Building(models.Model):
    """
    building_id,name,admin,rooms
    305,IT / BT,공과대학,19
    """
    building_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    admin = models.CharField(max_length=100)
    rooms = models.IntegerField()


class Course(models.Model):
    """
    course_id,name,credit
    CIE3022,철근콘크리트구조설계,3
    """
    course_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    credit = models.IntegerField()

# ----------- Tier 2 ---------------

class Class(models.Model):
    """
    class_id,class_no,course_id,name,major_id,year,credit,lecturer_id,person_max,opened,room_id
    8831,10003,CIE3022,철근콘크리트구조설계,1,1,3,2001001001,3,2022,169
    """
    class_id = models.IntegerField(primary_key=True)
    class_no = models.IntegerField()
    # course_id: FK
    # name = models.CharField(max_length=100) : DB 스키마에서 삭제 가능 과목에 이미 있음
    # major_id: FK, DB 스키마에서 화살표 빠진거 보충 필요
    year = models.IntegerField()
    # credit = models.IntegerField() :  DB 스키마에서 삭제 가능 과목에 이미 있음
    # lecturer_id: FK
    person_max = models.IntegerField()
    opened = models.IntegerField()
    enrolled = models.IntegerField(default=0) # 추가 가능
    # room_id: FK

# ----------- Tier 3 ---------------
# ----------- Tier 4 ---------------
