from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL

from main_app.maangers import DirectorManager
from main_app.mixins import AwardedMixin, UpdatedMixin


# Create your models here.
class Base(models.Model):
    full_name = models.CharField(validators=[MinLengthValidator(2)],
                                 max_length=120)
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')

    class Meta:
        abstract = True

class Director(Base):
    years_of_experience = models.SmallIntegerField(validators=[MinValueValidator(0)],default=0)
    objects = DirectorManager() #when we do it we don't migrate because we are not changing anything in the base


class Actor(Base,AwardedMixin,UpdatedMixin):
    pass


class Movie(AwardedMixin,UpdatedMixin):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(validators=[MinLengthValidator(5)],max_length=150)
    release_date = models.DateField()
    storyline = models.TextField(null=True,blank=True)
    genre = models.CharField(choices=GenreChoices.choices,max_length=6,default=GenreChoices.OTHER)
    rating  = models.DecimalField(decimal_places=1, max_digits=3,
                                  validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
                                  default=0.0)
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(Director, on_delete=models.CASCADE,related_name='director_movies')  #one to many
    starring_actor = models.ForeignKey(Actor, on_delete=SET_NULL,null=True,blank=True,related_name='starring_movies')
    actors = models.ManyToManyField(Actor,related_name='actors_movies')
