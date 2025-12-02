from django.db import models
from django.db.models.aggregates import Count


class PublisherManager(models.Manager):
    def get_publishers_by_books_count(self):
        publishers_by_book = (self.annotate(book_count =Count('books_publisher')).
                              order_by('-book_count','name'))
        return publishers_by_book