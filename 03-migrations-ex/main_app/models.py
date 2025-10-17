from django.db import models

# Create your models here.
class Shoe(models.Model):
    brand = models.CharField(max_length=25)
    size = models.PositiveIntegerField()

#python manage.py makemigrations main_app --name migrate_unique_brands --empty
class UniqueBrand(models.Model):
    brand = models.CharField(max_length=25)
