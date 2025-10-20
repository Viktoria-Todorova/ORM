from django.db import models


class LaptopChoices(models.TextChoices):
    ASUS = "Asus", "Asus"
    ACER = "Acer", "Acer"
    APPLE = "Apple", "Apple"
    LENOVO = "Lenovo", "Lenovo"
    DELL = "Dell", "Dell"


class OperationSystemChoices(models.TextChoices):
    WINDOWS = "Windows", "Windows"
    MACOS = "MacOS", "MacOS"
    LINUX = "Linux", "Linux"
    CHROMEOS = "Chrome OS", "Chrome OS"

class MealTypeChoices(models.TextChoices):
    BREAKFAST = "Breakfast", "Breakfast"
    LUNCH = "Lunch", "Lunch"
    DINNER = "Dinner", "Dinner"
    SNACK = "Snack", "Snack"

class DificultyChoices(models.TextChoices):
    EASY = "Easy", "Easy"
    MEDIUM = "Medium", "Medium"
    HARD = "Hard", "Hard"

class WorkoutTypeChoices(models.TextChoices):

    CARDIO = 'Cardio', 'Cardio'
    STRENGTH = 'Strength', 'Strength'
    YOGA = 'Yoga', 'Yoga'
    CROSSFIT = 'CrossFit', 'CrossFit'
    CALISTHENICS = 'Calisthenics', 'Calisthenics'