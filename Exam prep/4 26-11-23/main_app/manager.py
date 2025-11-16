from django.db import models
from django.db.models import Count



class AuthorsManager(models.Manager):
    def get_authors_by_article_count(self):
        authors = self.annotate(author_count=Count('articles_authors')).order_by('-author_count','email')
        return authors