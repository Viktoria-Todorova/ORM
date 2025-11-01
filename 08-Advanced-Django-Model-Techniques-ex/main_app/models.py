from decimal import Decimal

from django.contrib.postgres.search import SearchVectorField
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator
from django.db import models

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import NameValidator, PhoneNumberValidator


# Create your models here.

#1

class Customer(models.Model):
    name= models.CharField(max_length=100,
                           validators=[NameValidator(message="Name can only contain letters and spaces")])

    age= models.PositiveIntegerField(
        validators=[MinValueValidator(18,message= "Age must be greater than or equal to 18")]
    )
    email= models.EmailField(
        error_messages={'invalid':"Enter a valid email address"}
    ) #because by default EmailField  checks the email so it doesnt need validator

    phone_number= models.CharField(max_length=13,
                                validators=[PhoneNumberValidator(message="Phone number must start with '+359' followed by 9 digits")])

    # RegexValidator(regex = r'^+359\d{9}$',message = '...')

    website_url = models.URLField(
        error_messages={'invalid': "Enter a valid URL"}
    )

#2
class BaseMedia(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created_at','title')

    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at  = models.DateTimeField(auto_now_add=True)

class Book(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"

    author = models.CharField(max_length=100,
                              validators=[MaxLengthValidator(50, message="Author must be at least 5 characters long")])
    isbn = models.CharField(max_length=20,
                            validators=[MaxLengthValidator(5, message="ISBN must be at least 6 characters long")])


class Movie(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"
    director = models.CharField(max_length=100,
                                validators=[MinLengthValidator(8, message= "Director must be at least 8 characters long")])

class Music(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"

    artist = models.CharField(max_length=100,
                              validators=[MinLengthValidator(9, message= "Artist must be at least 9 characters long")])


#3
class Product(models.Model):
    TAX_PERCENTAGE :Decimal = Decimal('0.08')
    SHIPPING_MULTIPLIER: Decimal = Decimal('2.00')
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def calculate_tax(self) -> Decimal:
        return self.price * self.TAX_PERCENTAGE

    def calculate_shipping_cost(self,weight: Decimal) -> Decimal:
        return  weight * self.SHIPPING_MULTIPLIER

    def format_product_name(self) -> str:
        return f"Product: {self.name}"



class DiscountedProduct(Product):
    PRICE_INCREASE :Decimal = Decimal('0.20')
    TAX_PERCENTAGE :Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER :Decimal = Decimal('1.50')
    class Meta:
        proxy = True #shares the same database table as its parent model "Product" and provides additional or customized functionality.

    def calculate_price_without_discount(self) -> Decimal:
        return Decimal(str(self.price)) * (1 + self.PRICE_INCREASE)

    def format_product_name(self):
        ...
        return f"Discounted Product: {self.name}"


#4

class Hero(models.Model,RechargeEnergyMixin):
    ABILITY_ENERGY_REQUIRED: int = 0
    MIN_ENERGY: int = 1

    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy =models.PositiveIntegerField()

    @property
    def required_energy_message(self) -> str:
        return ""

    @property
    def succsesful_ability_use_message(self)-> str:
        return ""

    def use_ability(self):
        if self.energy < self.ABILITY_ENERGY_REQUIRED:
            return self.required_energy_message

        if self.energy - self.ABILITY_ENERGY_REQUIRED > 0:
            self.energy -= self.ABILITY_ENERGY_REQUIRED
        else:
            self.energy = self.MIN_ENERGY
        self.save()
        return self.succsesful_ability_use_message

class SpiderHero(Hero):
    ABILITY_ENERGY_REQUIRED : int = 80

    class Meta:
        proxy = True

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def succsesful_ability_use_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    def swing_from_buildings(self) -> str:
        return self.use_ability()


class FlashHero(Hero):
    ABILITY_ENERGY_REQUIRED: int = 60

    class Meta:
        proxy = True

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def succsesful_ability_use_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"


    def run_at_super_speed(self):
        return self.use_ability()


#5
class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    search_vector  = SearchVectorField(null=True,
                                       db_index=True, )
