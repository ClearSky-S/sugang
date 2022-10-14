import datetime

from django.core.management.base import BaseCommand, CommandError
from home.models import *
import csv

class Command(BaseCommand):
    help = 'inserts test data set'

    def handle(self, *args, **options):
        print("insert test data set")

        # ----------- Tier 1 ---------------
        # Tier 1 Model: 전공, 건물, 과목
        print("Tier 1 Model: 전공, 건물, 과목")
        print("insert major.csv")
        with open('test_data/csv/major.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'major_id':
                    continue
                major = Major()
                """
                major_id,name
                1,건설환경공학과
                """
                major.major_id = row[0]
                major.name = row[1]
                major.save()

        print("insert building.csv")
        with open('test_data/csv/building.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'building_id':
                    continue
                building = Building()
                """
                building_id,name,admin,rooms
                305,IT / BT,공과대학,19
                """
                building.building_id = row[0]
                building.name = row[1]
                building.admin = row[2]
                building.rooms = row[3]
                building.save()

        print("insert course.csv")
        with open('test_data/csv/course.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'course_id':
                    continue
                course = Course()
                """
                course_id,name,credit
                CIE3022,철근콘크리트구조설계,3
                """
                course.course_id = row[0]
                course.name = row[1]
                course.credit = row[2]
                course.save()

        # ----------- Tier 2 ---------------
        # Tier 2 Model: 교강사, 강의실
        print("Tier 2 Model: 교강사, 강의실")

        print("insert lecturer.csv")
        with open('test_data/csv/lecturer.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'lecturer_id':
                    continue
                lecturer = Lecturer()
                """
                lecturer_id,name,major_id
                2001001001,조병완,1
                """
                lecturer.lecturer_id = row[0]
                lecturer.name = row[1]
                lecturer.major_id = row[2]
                lecturer.save()

        print("insert room.csv")
        with open('test_data/csv/room.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'room_id':
                    continue
                room = Room()
                """
                room_id,building_id,occupancy
                1,305,140
                """
                room.room_id = row[0]
                room.building_id = row[1]
                room.occupancy = row[2]
                room.save()

        # ----------- Tier 3 ---------------
        # Tier 3 Model: 학생, 수업
        print("Tier 3 Model: 학생, 수업")

        print("insert student.csv")
        with open('test_data/csv/student.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'student_id':
                    continue
                student = Student()
                """
                student_id,password,name,sex,major_id,lecturer_id,year
                2018003125,125125125,정남아,female,44,2001032011,4
                """
                student.student_id = row[0]
                student.name = row[2]
                student.sex = row[3]
                student.major_id = row[4]
                student.lecturer_id = row[5]
                student.year = row[6]
                student.save()
                # Auth
                user = User()
                user.username = row[0]
                user.student_id = row[0]
                user.first_name = row[2]
                user.set_password(row[1])  # SHA256 방식으로 암호화 되어 비밀번호가 저장된다.
                user.save()

        print("insert class.csv")
        with open('test_data/csv/class.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'class_id':
                    continue
                clas = Class()
                """
                csv:
                class_id,class_no,course_id,(name),major_id,year,(credit),lecturer_id,person_max,opened,room_id
                8831,10003,CIE3022,철근콘크리트구조설계,1,1,3,2001001001,3,2022,169
                DB:
                class_id,class_no,course_id,major_id,year,(credit),lecturer_id,person_max,opened,room_id, students
                8831,10003,CIE3022,1,1,2001001001,3,2022,169, OneToManyField
                """
                clas.class_id = row[0]
                clas.class_no = row[1]
                clas.course_id = row[2]
                # clas.name = row[3]
                clas.major_id = row[4]
                clas.year = row[5]
                # clas.credit = row[6]
                clas.lecturer_id = row[7]
                clas.person_max = row[8]
                clas.opened = row[9]
                clas.room_id = row[10]
                clas.save()

        # ----------- Tier 4 ---------------
        # Tier 4 Model: 성적, 수업시간
        print("Tier 4 Model: 성적, 수업시간")

        print("insert credits.csv")
        with open('test_data/csv/credits.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'credits_id':
                    continue
                credits = Credits()
                """
                credits_id,student_id,course_id,year,grade
                1,2018003125,GEN5026,2022,B0
                """
                credits.credits_id = row[0]
                credits.student_id = row[1]
                credits.course_id = row[2]
                credits.year = row[3]
                credits.grade = row[4]
                credits.save()


        print("insert time.csv")
        with open('test_data/csv/time.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                if row[0] == 'time_id':
                    continue
                time1 = Time()
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
                time1.time_id = row[0]
                time1.classInfo_id = row[1]
                time1.period = row[2]
                if row[3] != "NO":
                    time1.day = row[3][9]
                    begin = row[3][11:16]
                    end = row[4][11:16]
                    time1.begin = datetime.time(int(begin[0:2]), int(begin[3:5]))
                    time1.end = datetime.time(int(end[0:2]), int(end[3:5]))
                time1.save()
