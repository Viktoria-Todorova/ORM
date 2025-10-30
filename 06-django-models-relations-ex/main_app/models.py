from datetime import timedelta

from django.db import models




# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=40)

# •	title - character field, consisting of a maximum of 40 characters.
# •	price - decimal field, with a maximum of 5 digits and 2 decimal places.
# •	author - many-to-one relation to the "Author" class. If an author is deleted, you should automatically delete all the related books



class Book(models.Model):

    title = models.CharField(max_length=40)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    """"
       FOREIGN KEY(author)
       REFERENCES main_app_author(id)
       ON DELETE CASCADE
    """
    author = models.ForeignKey(Author,on_delete=models.CASCADE)


#2
# Music App
# Write a Django model called "Song" with the provided fields:
# •	title - character field, consisting of a maximum of 100 characters, unique.
# Write a second Django model called "Artist" with the provided fields:
# •	name - character field, consisting of a maximum of 100 characters, unique.
# •	songs - many-to-many relation to the "Song" class. The field has a related name set to "artists".

class Song(models.Model):
    title = models.CharField(max_length=100,unique=True)

class Artist(models.Model):
    name = models.CharField(max_length=100,unique=True)
    songs=models.ManyToManyField(Song,related_name="artists") #it creates mapping table


#3
# Write a Django model called "Product" with the provided field:
# •	name - character field, consisting of a maximum of 100 characters, unique.
# Write a second Django model called "Review" with the provided fields:
# •	description - text field, consisting of a maximum of 200 characters.
# •	rating – positive small integer field.
# •	product - many-to-one relation to the "Product" class. If a product is deleted, you should automatically delete all the related reviews. The field has a related name set to "reviews".

class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)

class Review(models.Model):
    description = models.TextField(max_length=200)
    rating= models.PositiveSmallIntegerField()
    product=models.ForeignKey(Product,related_name="reviews",on_delete=models.CASCADE)


#4

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField()
    driver=models.OneToOneField(Driver,on_delete=models.CASCADE,related_name="license")

    def __str__(self):
        expiration_date = self.issue_date + timedelta(days=365)
        return f"License with number: {self.license_number} expires on {expiration_date}!"


# 5
#
# Write a Django model called "Owner" with the provided information:
# •	name - character field, consisting of a maximum of 50 characters.
# Write a second Django model called "Car" with the provided information:
# •	model - character field, consisting of a maximum of 50 characters.
# •	year - positive integer field.
# •	owner - many-to-one relation to the "Owner" class. If an owner is deleted, you should automatically delete all the related cars. The field is optional and has a related name set to "cars".
# Write a third Django model called "Registration" with the provided information:
# •	registration_number - character field, consisting of a maximum of 10 characters, unique.
# •	registration_date - date field, optional.
# •	car - one-to-one relation to the "Car" class. If a car is deleted, you should automatically delete the related registration. The field is optional and has a related name set to "registration".

class Owner(models.Model):
    name = models.CharField(max_length=50)

class Car(models.Model):
    model = models.CharField(max_length=50)
    year= models.PositiveIntegerField()
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE,blank=True,null=True,related_name="cars")

class Registration(models.Model):
    registration_number=models.CharField(max_length=10, unique=True)
    registration_date=models.DateField(blank=True,null=True)#optional
    car=models.OneToOneField(Car,on_delete=models.CASCADE,related_name="registration",blank=True,null=True)
