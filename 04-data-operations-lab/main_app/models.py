from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=20)
    gender =models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    salary=models.IntegerField()
    department = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.age} {self.gender} {self.city} {self.salary} {self.department}'