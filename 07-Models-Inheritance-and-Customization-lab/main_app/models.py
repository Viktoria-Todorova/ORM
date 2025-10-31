from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from main_app.fields import BooleanChoiceField


# Create your models here.

# •	name
# o	A character field.
# o	It has a maximum length of 100 characters.
# o	Represents the name of the animal.
# •	species
# o	A character field.
# o	It has a maximum length of 100 characters.
# o	Represents the species of the animal.
# •	birth_date
# o	A date field.
# o	Represents the date of birth of the animal.
# •	sound
# o	A character field.
# o	It has a maximum length of 100 characters.
# o	Represents the sound that the animal makes.

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound =models.CharField(max_length=100)

    @property
    def age(self):
        age =date.today() - self.birth_date
        return age.days // 365

# create 3 more models: "Mammal", "Bird", and "Reptile" - all of them are types of animals:
# •	The mammal has an additional character field called "fur_color" with a maximum length of 50 chars.
# •	The bird has an additional decimal field called "wing_span" that can store up to 5 digits and has exactly 2 decimal places.
# •	The reptile has an additional character field called "scale_type" with a maximum length of 50 chars.

class Mammal(Animal):
    fur_color = models.CharField(max_length=50)

class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)

class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

class ZooKeeper(Employee):
    class SpecialityChoices(models.TextChoices):
        MAMMALS = 'Mammals', 'Mammals'
        BIRDS = 'Birds', 'Birds'
        REPTILES = 'Reptiles', 'Reptiles'
        OTHERS = 'Others', 'Others'

    specialty = models.CharField(max_length=10, choices=SpecialityChoices.choices)
    managed_animals = models.ManyToManyField(Animal)

#4
    # Create a validation to ensure that the object is checked against the given list of
    # valid choices ("SPECIALITIES"). If the specialty is not a valid choice,
    # a ValidationError should be raised with the message: "Specialty must be a valid choice.".
    def clean(self):
        if self.specialty not in self.SpecialityChoices:
            raise ValidationError("Specialty must be a valid choice.")
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

#3
# It inherits from the "Animal" model but does NOT have its own database table.
# Its primary purpose is to extend the "Animal" model behavior.
# Currently, it is NOT needed to add additional logic to the model.
class ZooDisplayAnimal(Animal):
    def display_info(self):
        return (f"Meet {self.name}! Species: {self.species},"
                f" born {self.birth_date}. It makes a noise like '{self.sound}'.")
    def is_endangered(self):
        species = ["Cross River Gorilla", "Orangutan","Green Turtle"]
        if self.species in species:
            return f"{self.species} is at risk!"
        else:
            return f"{self.species} is not at risk."

    class Meta:
        proxy = True
