import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Owner, Car, \
    Registration
from django.db.models import QuerySet
from datetime import timedelta, datetime, date


# Create queries within functions

#1 Library
def show_all_authors_with_their_books()->str:
    #() returns a string with authors and their books, separated by comma and space
    # - ", ", ordered by the id of the author (ascending) as follows:


    #best option
    # authors_books = Author.objects.prefetch_related('book_set').order_by('id')
    # print(authors_books)

    ordered_authors= Author.objects.all().order_by("id") #all authors
    author_books = []
    for author in ordered_authors:
        books = Book.objects.filter(author=author)
        if not books:
            continue

        titles = ', '.join(b.title for b in books)
        author_books.append(f"{author.name} has written - {titles}!")

    return  "\n".join(author_books)

def delete_all_authors_without_books():
    """
    SELECT * FROM "main_app_author"
    LEFT OUTER JOIN "main_app_book"
    ON( main_app_author.id = main_app_book.author_id)
    WHERE main_app_book.id IS NULL
    """
    Author.objects.filter(book__isnull=True).delete()

# # Display authors and their books
# authors_with_books = show_all_authors_with_their_books()
# print(authors_with_books)
#
# # Delete authors without books
# delete_all_authors_without_books()
# print(Author.objects.count())
#
#

#2
#add_song_to_artist(artist_name: str, song_title: str) gets the artist object by the artist's name and the song object by the song's title, and adds the song object to the artist's songs collection.
#get_songs_by_artist(artist_name: str) returns all the song objects from the songs collection in a queryset, ordered by song id (descending) for the given artist.
#remove_song_from_artist(artist_name: str, song_title: str) gets the artist object by the artist's name and the song object by the song's title, and removes the song object from the artist's songs collection

def add_song_to_artist(artist_name: str, song_title: str)->None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)

def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.all().order_by("-id")

def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)

# # Create artists
# artist1 = Artist.objects.create(name="Daniel Di Angelo")
# artist2 = Artist.objects.create(name="Indila")
# # Create songs
# song1 = Song.objects.create(title="Lose Face")
# song2 = Song.objects.create(title="Tourner Dans Le Vide")
# song3 = Song.objects.create(title="Loyalty")

# # Add a song to an artist
# add_song_to_artist("Daniel Di Angelo", "Lose Face")
# add_song_to_artist("Daniel Di Angelo", "Loyalty")
# add_song_to_artist("Indila", "Tourner Dans Le Vide")

# # Get all songs by a specific artist
# songs = get_songs_by_artist("Daniel Di Angelo")
# for song in songs:
#     print(f"Daniel Di Angelo: {song.title}")
#
# # Get all songs by a specific artist
# songs = get_songs_by_artist("Indila")
# for song in songs:
#     print(f"Indila: {song.title}")

# # Remove a song from an artist
# remove_song_from_artist("Daniel Di Angelo", "Lose Face")
#
# # Check if the song is removed
# songs = get_songs_by_artist("Daniel Di Angelo")
#
# for song in songs:
#     print(f"Songs by Daniel Di Angelo after removal: {song.title}")



#3
# calculate_average_rating_for_product_by_name(product_name: str) returns the calculated average rating for a given product by its name.
# get_reviews_with_high_ratings(threshold: int) returns all reviews with greater than or equal ratings to the threshold.
# get_products_with_no_reviews() returns all products that do NOT have any related reviews, ordered by product name (descending).
# delete_products_without_reviews() deletes all the products that do not have any related reviews.
# Examples

def calculate_average_rating_for_product_by_name(product_name: str) ->float:
    """
    SELECT * FROM product
    WHERE name=product_name

    SELECT AVG(rating) FROM review
    WHERE product_id = product_id
    """
    # product = Product.objects.annotate(avg_review_score= Avg('reviews__rating')).get(name=product_name)

    product = Product.objects.get(name=product_name)
    reviews=product.reviews.all()
    total_rating= sum(r.rating for r in reviews)/len(reviews)
    return total_rating
    # return  product.avg_review_score

def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    return Review.objects.filter(rating__gte=threshold)

def get_products_with_no_reviews() -> QuerySet[Product]:
    """"
    SELECT * FROM product AS p
    LEFT JOIN reviews AS r
    ON p.id = r.product_id
    WHERE r.id is NULL
    ORDER BY name desc
    """
    return Product.objects.filter(reviews__isnull=True).order_by("-name")

def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()

# # Create some products
# product1 = Product.objects.create(name="Laptop")
# product2 = Product.objects.create(name="Smartphone")
# product3 = Product.objects.create(name="Headphones")
# product4 = Product.objects.create(name="PlayStation 5")
#
# # Create some reviews for products
# review1 = Review.objects.create(description="Great laptop!", rating=5, product=product1)
# review2 = Review.objects.create(description="The laptop is slow!", rating=2, product=product1)
# review3 = Review.objects.create(description="Awesome smartphone!", rating=5, product=product2)

# # Run the function to get products without reviews
# products_without_reviews = get_products_with_no_reviews()
# print(f"Products without reviews: {', '.join([p.name for p in products_without_reviews])}")
# # Run the function to delete products without reviews
# delete_products_without_reviews()
# print(f"Products left: {Product.objects.count()}")
#
# # Calculate and print the average rating
# print(calculate_average_rating_for_product_by_name("Laptop"))


#4

def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by("-license_number")
    return  "\n".join(str(l) for l in licenses)

def get_drivers_with_expired_licenses(due_date: datetime.date) -> QuerySet[Driver]:
    latest_possible_issue_date = due_date - timedelta(days=365)
    drivers_with_expired_license = Driver.objects.filter(
        license__issue_date__lte=latest_possible_issue_date)

    return drivers_with_expired_license

# # Create drivers
# driver1 = Driver.objects.create(first_name="Tanya", last_name="Petrova")
# driver2 = Driver.objects.create(first_name="Ivan", last_name="Yordanov")
#
# # Create licenses associated with drivers
# license1 = DrivingLicense.objects.create(license_number="123", issue_date=date(2022, 10, 6), driver=driver1)
#
# license2 = DrivingLicense.objects.create(license_number="456", issue_date=date(2022, 1, 1), driver=driver2)
# #
# Calculate licenses expiration dates
# expiration_dates = calculate_licenses_expiration_dates()
# print(expiration_dates)
#
# # Get drivers with expired licenses
# drivers_with_expired_licenses = get_drivers_with_expired_licenses(date(2023, 1, 1))
#
# for driver in drivers_with_expired_licenses:
#     print(f"{driver.first_name} {driver.last_name} has to renew their driving license!")

#5
def register_car_by_owner(owner: Owner) -> str:
    car = Car.objects.filter(registration__isnull=True).first()
    registration= Registration.objects.filter(car__isnull=True).first()
    car.owner = owner
    car.registration = registration
    car.save()
    registration.registration_date = datetime.today()
    registration.car = car
    registration.save()
    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."


# Create owners
# owner1 = Owner.objects.create(name='Ivelin Milchev')
# owner2 = Owner.objects.create(name='Alice Smith')
#
# # Create cars
# car1 = Car.objects.create(model='Citroen C5', year=2004)
# car2 = Car.objects.create(model='Honda Civic', year=2021)
# # Create instances of the Registration model for the cars
# registration1 =  Registration.objects.create(registration_number='TX0044XA')
# registration2 = Registration.objects.create(registration_number='XYZ789')
#
# print(register_car_by_owner(owner1))


