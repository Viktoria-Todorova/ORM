from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.manager import AstronautManager
from main_app.validators import PhoneNumberValidator


# Create your models here.
class Base(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=120,
                            validators=[MinLengthValidator(2)])
    class Meta:
        abstract = True
# class LaunchTime(models.Model):
#

class Astronaut(Base):

    # 	Validation: Must contain only digits
    phone_number = models.CharField(max_length=15,
                                    validators=[PhoneNumberValidator()],
                                    unique=True) #todo
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(blank=True, null=True)
    spacewalks =models.IntegerField(default=0,validators=[MinValueValidator(0)])
    objects = AstronautManager()
class Spacecraft(Base):
    manufacturer = models.CharField(max_length=100,)
    capacity =models.SmallIntegerField(validators=[MinValueValidator(1)])
    weight =models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateTimeField(auto_now=True)
class Mission(Base):
    class StatusChoices(models.TextChoices):
        PLANNED ='Planned','Planned'
        ONGOING = 'Ongoing','Ongoing'
        COMPLETED = 'Completed','Completed'

    description=models.TextField(blank=True,null=True)
    status =models.CharField(choices=StatusChoices.choices,max_length=9,default=StatusChoices.PLANNED)
    launch_date = models.DateTimeField(auto_now=True)
    spacecraft = models.ForeignKey(Spacecraft,on_delete=models.CASCADE, related_name='missions_spacecraft')
    astronauts= models.ManyToManyField(Astronaut,related_name='missions_astronauts')
    commander =models.ForeignKey(Astronaut,on_delete=models.SET_NULL,blank=True,null=True, related_name='missions_commander')
#     	Establishes a many-to-one relationship with the Astronaut model, indicating the mission commander


