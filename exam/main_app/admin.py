from django.contrib import admin

# Register your models here.

from main_app.models import Book, Publisher, Author


# Register your models here.
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name','established_date','country','rating']
    filter = ['rating']
    search_fields = ['name','country']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name','birth_date','country','is_active']
    filter = ['is_active']
    search_fields = ['name','country']
    readonly_fields = ['updated_at']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','price','summary','main_author','publisher']
    filter=[ 'publication_date','is_bestseller','genre']
    search_fields =['title','main_author__name','publisher__name']
    readonly_fields = ['updated_at']