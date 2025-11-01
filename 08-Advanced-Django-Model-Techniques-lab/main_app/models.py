from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.validator import validate_menu_categories


# Create your models here.
class ReviewMixin(models.Model):
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)]
    )
    class Meta:
        abstract = True


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2,message ='Name must be at least 2 characters long.'),
            MaxLengthValidator(100,message="Name cannot exceed 100 characters.")
        ])

    location = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2,message="Location must be at least 2 characters long."),
            MaxLengthValidator(100,message="Location cannot exceed 200 characters.")
        ])
    description = models.TextField(null=True,blank=True)
    rating = models.DecimalField(max_digits=3,decimal_places=2,
                                 validators=[
                                     MinValueValidator(0,message="Rating must be at least 0.00."),
                                     MaxValueValidator(5,message="Rating cannot exceed 5.00.")
                                 ])

#2
class Menu(models.Model):
    name = models.CharField(
        max_length=100
    )
    description =models.TextField(validators=[validate_menu_categories])
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

#3
# •	A default ordering in descending order for the model's database queries on the field "rating".
# •	A human-readable name for the model in the admin interface - "Restaurant Review".
# •	A human-readable plural name for the model in the admin interface - "Restaurant Reviews".
# •	That NO two records for the fields "reviewer_name" and "restaurant" should share the same combination of values.
class RestaurantReview(ReviewMixin):
    # reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    review_content = models.TextField()
    # rating = models.PositiveIntegerField(
    #     validators=[MaxValueValidator(5)]
    # )

    class Meta:
        abstract = True #important for it to be inherited
        ordering = ['-rating']
        verbose_name='Restaurant Review'
        verbose_name_plural='Restaurant Reviews'
        unique_together = (('reviewer_name', 'restaurant'),)

class RegularRestaurantReview(RestaurantReview):
    pass

class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)
    class Meta(RestaurantReview.Meta):

        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'


#5
class MenuReview(ReviewMixin):
    # reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
    review_content = models.TextField()
    # rating = models.PositiveIntegerField(
    #     validators=[MaxValueValidator(5)]
    # )

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = (('reviewer_name', 'menu'),)
        indexes = [models.Index(fields=['menu'],name = 'main_app_menu_review_menu_id'),
                 ]

