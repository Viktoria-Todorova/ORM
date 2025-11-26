
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from main_app.manager import HouseManager


# Create your models here.

class House(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(5)],
    )

    motto = models.TextField(
        blank=True,
        null=True,
    )

    is_ruling = models.BooleanField(
        default=False
    )

    castle = models.CharField(
        max_length=80,
        blank=True,
        null=True,
    )

    wins = models.PositiveSmallIntegerField(
        default=0,
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )
    objects = HouseManager()
    def __str__(self):
        return self.name

class Dragon(models.Model):
    class BreathChoices(models.TextChoices):
        FIRE = "Fire", "Fire"
        ICE = "Ice", "Ice"
        LIGHTNING = "Lightning", "Lightning"
        UNKNOWN = "Unknown", "Unknown"

    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(5)],
    )

    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=1.0,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0),
        ]
    )

    breath = models.CharField(
        max_length=9,
        choices=BreathChoices.choices,
        default=BreathChoices.UNKNOWN,
    )

    is_healthy = models.BooleanField(
        default=True
    )

    birth_date = models.DateField(
        auto_now=True
    )

    wins = models.PositiveSmallIntegerField(
        default=0,
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name='dragons'
    )




class Quest(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[MinLengthValidator(5)]
    )

    code = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z#]{4}$'
            )
        ]
    )

    reward = models.FloatField(
        default=100.0
    )

    start_time = models.DateTimeField()

    modified_at = models.DateTimeField(
        auto_now=True
    )

    dragons = models.ManyToManyField(
        'Dragon',
        related_name='quests'
    )

    host = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name='quests_hosted'
    )