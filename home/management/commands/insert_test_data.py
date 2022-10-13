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
                        user.set_password(row[1])
                        user.save()

