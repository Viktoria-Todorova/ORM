from django.db import models

from orm_skeleton.choices import RoomTypeChoices, CharactersChoices


#from main_app.orm_skeleton.choices import RoomTypeChoices


# Create your models here.
#1
class Pet(models.Model):
    name = models.CharField(max_length=40)
    species = models.CharField(max_length=40)

#2
class Artifact(models.Model):
    name = models.CharField(max_length=70)
    origin = models.CharField(max_length=70)
    age=models.PositiveIntegerField()
    description=models.TextField()
    is_magical=models.BooleanField(default=False)

#3
class Location(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    population = models.PositiveIntegerField()
    description=models.TextField()
    is_capital=models.BooleanField(default=False)

#4
class Car(models.Model):
    model = models.CharField(max_length=40)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=40)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    price_with_discount = models.DecimalField(decimal_places=2, max_digits=10,default=0)
#5
class Task(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    due_date = models.DateField()
    is_finished = models.BooleanField(default=False)


#6.	Hotel Room
# •	room_number - positive integer field.
# •	room_type - character field, consisting of a maximum of 10 characters with choices - "Standard", "Deluxe", and "Suite".
# •	capacity - positive integer field.
# •	amenities - text field.
# •	price_per_night - decimal field with a maximum of 8 digits and 2 decimal places.
# •	is_reserved - boolean field with default value "False".


class HotelRoom(models.Model):


    room_number =models.PositiveIntegerField()
    room_type = models.CharField(max_length=10,choices = RoomTypeChoices,)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(decimal_places=2, max_digits=8)
    is_reserved = models.BooleanField(default=False)


#•	name - character field, consisting of a maximum of 100 characters.
# •	class_name - character field, consisting of a maximum of 20 characters, with choices - "Mage", Warrior", "Assassin", and "Scout".
# •	level - positive integer field.
# •	strength - positive integer field.
# •	dexterity - positive integer field.
# •	intelligence - positive integer field.
# •	hit_points - positive integer field.
# •	inventory - text field.


class Character(models.Model):
    name = models.CharField(max_length=100)
    class_name= models.CharField(max_length=20,choices=CharactersChoices)
    level = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    dexterity = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    hit_points = models.PositiveIntegerField()
    inventory =models.TextField()
