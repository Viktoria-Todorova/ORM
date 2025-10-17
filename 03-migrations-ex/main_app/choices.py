from django.db import models
class OrderStatusChoices(models.TextChoices):
    PENDING = "P",'Pending'
    COMPLETED = "C",'Completed'
    CANCELED = "CA",'Canceled'