import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Employee, Student
from django.db import connection,reset_queries

# FC5204	John	Doe	15/05/1995	john.doe@university.com
# FE0054	Jane	Smith	null	jane.smith@university.com
# FH2014	Alice	Johnson	10/02/1998	alice.johnson@university.com
# FH2015	Bob	Wilson	25/11/1996	bob.wilson@university.com

# Run and print your queries
class Students:
    pass
#1.	Add Students

def add_students():
    Student.objects.create(
        student_id = "FC5204",
        first_name = "John",
        last_name = "Doe",
        birth_date = datetime.strptime("15/05/1995", "%d/%m/%Y").date(),
        email = 'john.doe@university.com'
    )
    Student.objects.create(
        student_id="FE0054",
        first_name="Jane",
        last_name="Smith",
        birth_date=None,
        email="jane.smith@university.com"
    )

    Student.objects.create(
        student_id="FH2014",
        first_name="Alice",
        last_name="Johnson",
        birth_date=datetime.strptime("10/02/1998", "%d/%m/%Y").date(),
        email="alice.johnson@university.com"
    )

    Student.objects.create(
        student_id="FH2015",
        first_name="Bob",
        last_name="Wilson",
        birth_date=datetime.strptime("25/11/1996", "%d/%m/%Y").date(),
        email="bob.wilson@university.com"
    )

#2.	Get Students Info
def get_students_info():
    all_students = Student.objects.all()
    return '\n'.join(f"Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}"for s in all_students)


print(get_students_info())

#3.	Update Students' Emails

def update_students_emails():
    all_students = Student.objects.all()
    for s in all_students:
        s.email= s.email.replace(s.email.split('@')[1],"uni-students.com")
        s.save()
    #Student.objects.bulk_update(all_students, ['email'])

#4.	Truncate Students

def truncate_students():
    Student.objects.all().delete()

    # all= Student.objects.all()
    # all.delete()

