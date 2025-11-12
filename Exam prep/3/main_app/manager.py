from django.db import models
from django.db.models import Count



class CustomerManager(models.Manager):
#This method retrieves and returns all profile objects with more than two orders
    def get_regular_customers(self):
        customers = self.annotate(orders_count = Count('orders')).filter(orders_count__gt = 2).order_by('-orders_count')
        return customers