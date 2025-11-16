from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.manager import AuthorsManager
# Create your models here.

class Author(models.Model):
    full_name = models.CharField(max_length=100,
                                 validators=[MinLengthValidator(3)])
    email = models.EmailField()
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2005)],
                                                  )
    website = models.URLField(null=True, blank=True)
    objects = AuthorsManager()

class Article(models.Model):
    class CategoryChoices(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(max_length=200,
                             validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    category = models.CharField(choices=CategoryChoices.choices,max_length=10,default=CategoryChoices.TECHNOLOGY)
    authors = models.ManyToManyField(Author, related_name='articles_authors')
    published_on = models.DateField(auto_now=True)

class Review(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.FloatField(validators=[MaxValueValidator(1.0),MaxValueValidator(5.0)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    published_on = models.DateField(auto_now=True,editable=False)