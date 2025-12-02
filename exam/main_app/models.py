from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.manager import PublisherManager


# Create your models here.


class Publisher(models.Model):
    name = models.CharField(max_length=100,
                            validators=[MinLengthValidator(3)])
    established_date = models.DateField(default='1800-01-01')
    country = models.CharField(max_length=40,
                               default='TBC')
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
                               default=0.0)
    objects = PublisherManager()

    def __str__(self):
        return self.name
class Author(models.Model):
    name = models.CharField(max_length=100,
                            validators=[MinLengthValidator(3)])
    birth_date=models.DateField(null=True, blank=True)
    country = models.CharField(max_length=40,default='TBC')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    class GenreChoices(models.TextChoices):
        FICTION = 'Fiction','Fiction'
        NONFICTION = 'Non-Fiction','Non-Fiction'
        OTHER = 'Other','Other'
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    publication_date =models.DateField()
    summary = models.TextField(blank=True, null=True)
    genre = models.CharField(choices=GenreChoices.choices,max_length=11,default=GenreChoices.OTHER)
    price = models.DecimalField(decimal_places=2, max_digits=6,
                                validators=[MinValueValidator(0.01),
                                            MaxValueValidator(9999.99)],
                                default=0.01

                                )
    rating = models.FloatField(validators=[MinValueValidator(0.0),
                                           MaxValueValidator(5.0)],
                               default=0.0)
    is_bestseller = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE,
                                related_name='books_publisher',)
    main_author = models.ForeignKey(Author,on_delete=models.CASCADE,
                                    related_name='books_main_author',)
    co_authors = models.ManyToManyField(Author,related_name='books_co_authors',)