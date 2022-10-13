from django.core.management.base import BaseCommand, CommandError
from home.models import *
import csv

class Command(BaseCommand):
    help = 'inserts test data set'

    def handle(self, *args, **options):
        print("insert major.csv")
        with open('test_data\csv\major.csv', 'r') as csvfile:
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
