import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book
from django.db.models import Q, Count, Avg, F, Sum


# Create queries within functions

def populate_db():

    publisher1 = Publisher.objects.create(
        name="Epic Reads",
        established_date='1923-05-15',
        country="USA",
        rating=4.94
    )

    publisher2 = Publisher.objects.create(
        name="Global Prints",
        country="Australia",
        # established_date default kicks in
        # rating default kicks in
    )

    publisher3 = Publisher.objects.create(
        name="Abrams Books",
        rating=1.05
        # country default
        # established_date default
    )


    author1 = Author.objects.create(
        name="Jack London",
        birth_date="1876-01-12",
        country="USA",
        is_active=False
    )

    author2 = Author.objects.create(
        name="Craig Richardson"
    )

    author3 = Author.objects.create(
        name="Ramsey Hamilton"
    )

    author4 = Author.objects.create(
        name="Luciano Ramalho"
    )



    adventures_python = Book.objects.create(
        title="Adventures in Python",
        publication_date='2015-06-01',
        summary="An engaging and detailed guide to mastering a popular programming language.",
        genre=Book.GenreChoices.NONFICTION,
        price=49.99,
        rating=4.8,
        is_bestseller=False,
        publisher=publisher1,
        main_author=author2
    )
    adventures_python.co_authors.add(author3)

    # 2. The Call of the Wild
    call_wild = Book.objects.create(
        title="The Call of the Wild",
        publication_date='1903-11-23',
        summary="A classic adventure story set during the Klondike Gold Rush.",
        genre=Book.GenreChoices.FICTION,
        price=29.99,
        rating=4.9,
        is_bestseller=True,
        publisher=publisher2,
        main_author=author1
    )
    call_wild.co_authors.add(author2)
    # 3. Django World
    django_world = Book.objects.create(
        title="Django World",
        publication_date='2025-01-01',
        summary="A comprehensive resource for advanced users of a web development framework.",
        genre=Book.GenreChoices.NONFICTION,
        price=90.00,
        rating=5.0,
        is_bestseller=False,
        publisher=publisher3,
        main_author=author4
    )
    django_world.co_authors.add(author3,author4)

# populate_db()


def get_publishers(search_string=None):
    if search_string is None:
        return "No search criteria."

    name = Q(name__icontains=search_string)
    country = Q(country__icontains=search_string)
    if name is not None or country is not None:

        query = name | country
    elif name is not None:
        query = name
    else:
        query = country

    publishers = Publisher.objects.filter(query).order_by(
        '-rating','name'
    )
    if not publishers:
        return  "No publishers found."

    final_text = []
    for p in publishers:
        countryp= "Unknown" if p.country == 'TBC' else p.country
        final_text.append(f'Publisher: {p.name}, country: {countryp}, rating: {p.rating:.1f}')

    return '\n'.join(final_text)
# print(Publisher.objects.get_publishers_by_books_count())
# print(get_publishers(search_string='p'))
# print(get_publishers(search_string=''))
# print(get_publishers(search_string=None))
# print(get_publishers(search_string='z'))
def get_top_publisher():

    publisher = Publisher.objects.get_publishers_by_books_count().first()
    if publisher is None:
        return "No publishers found."
    return f"Top Publisher: {publisher.name} with {publisher.book_count} books."
# print(get_top_publisher())



def get_top_main_author():
    author = (Author.objects.annotate(count_books =Count('books_main_author')).
              order_by('-count_books','name')).first()
    if not author or author.count_books == 0:
        return "No results."
    books = author.books_main_author.all().order_by('title')
    final_b = ', '.join(n.title for n in books)
    avg_rating = books.aggregate(Avg('rating'))['rating__avg']
    return (f"Top Author: {author.name}, "
            f"own book titles: {final_b}, "
            f"books average rating: {avg_rating:.1f}")


# get_top_main_author()

def get_authors_by_books_count():
    authors = Author.objects.annotate(main_count_books = Count('books_main_author'),
                                      co_count_books = Count('books_co_authors')
                                      ).annotate(count_books = F('main_count_books')+ F('co_count_books')).order_by('-count_books','name')[:3]
    if not authors or authors[0].count_books == 0:
        return "No results."
    final_text = []
    for a in authors:

        final_text.append(f'{a.name} authored {a.count_books} books.')

    # o	If the authors' total number is less than three, display all in the described order.
    return '\n'.join(final_text)

# print(get_authors_by_books_count())

def get_bestseller():
    bestseller = Book.objects.filter(is_bestseller =True).annotate(
        num_authors = Count('co_authors') +1,
        composite_index = F('rating') + (Count('co_authors') + 1)
    ).order_by('composite_index','-rating','num_authors','title').first()
    if not bestseller:
        return "No results."
    co_authors = bestseller.co_authors.all().order_by('name')
    if not co_authors:
        authors_co = 'N/A'
    else:
        authors_co = '/'.join(a.name for a in co_authors)

    return (f"Top bestseller: {bestseller.title}, "
            f"index: {bestseller.composite_index:.1f}. "
            f"Main author: {bestseller.main_author.name}, . "
            f"Co-authors: {authors_co}.")
# print(get_bestseller())

def increase_price():
    books = (Book.objects.annotate(composite_sum = F('rating') + F('publisher__rating')).
             filter(publication_date__year=2025,composite_sum__gte=8.0))
    if not books.exists():
        return "No changes in price."

    for b in books:
        if b.price > 50.00:
            b.price = F('price') + 0.1

        else:
            b.price = F('price') + 0.2
        b.save()

    num_of_updated_books = books.count()
    return f"Prices increased for {num_of_updated_books} book/s."

print(increase_price())