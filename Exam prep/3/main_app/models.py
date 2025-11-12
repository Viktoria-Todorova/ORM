from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.manager import CustomerManager


# Create your models here.
class BaseModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Profile(BaseModel):
    full_name = models.CharField(max_length=100,
                                 validators=[MinLengthValidator(2)])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15,) #	Additional Note: This field is typically a string to accommodate various phone number formats.
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    objects = CustomerManager()


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(0.01)])
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

class Order(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name = 'orders')
    products = models.ManyToManyField(Product,related_name='products_ordered')
    total_price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])
    is_completed = models.BooleanField(default=False)