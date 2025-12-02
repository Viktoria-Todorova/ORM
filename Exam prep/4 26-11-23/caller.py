import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review
from django.db.models import Q, Count, Avg


# a1 = Author.objects.create(full_name="Alice Johnson", email="alice@mail.com", birth_year=1990)
# a2 = Author.objects.create(full_name="Bob Smith", email="bob@mail.com", birth_year=1980)
# a3 = Author.objects.create(full_name="Carla Green", email="carla@mail.com", birth_year=1975)
# art1 = Article.objects.create(title="AI in 2025", content="Deep learning is evolving rapidly...", category="Technology")
# art1.authors.add(a1, a2)
#
# art2 = Article.objects.create(title="Quantum Discoveries", content="Quantum computing leaps ahead...", category="Science")
# art2.authors.add(a3)
# Review.objects.create(content="Excellent article!", rating=5.0, author=a1, article=art1)
# Review.objects.create(content="Very informative.", rating=4.5, author=a2, article=art1)
# Review.objects.create(content="A fascinating read.", rating=4.0, author=a3, article=art2)

# Create queries within functions

def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)
    if search_name is not None and search_email is not None:
        query = query_name & query_email
    elif search_name is not None:
        query = query_name
    else:
        query= query_email

    authors = Author.objects.filter(query).order_by('-full_name')
    if not authors:
        return ''

    final_line = []

    for a in authors:
        final_line.append(f'Author: {a.full_name}, email: {a.email}, status: {"Banned" if a.is_banned  else "Not Banned"}')

    return '\n'.join(final_line)

# print(get_authors("Bob", ""))

def get_top_publisher():
    top_publisher = (Author.objects.annotate(num_of_articles = Count('articles_authors')).
                     order_by('-num_of_articles','email')).first()
    if top_publisher is None or top_publisher.num_of_articles == 0:
        return ''

    return f"Top Author: {top_publisher.full_name} with {top_publisher.num_of_articles} published articles."

# print(get_top_publisher())

def get_top_reviewer():
    top_reviewer = Author.objects.get_authors_by_article_count().first()
    if top_reviewer is None or top_reviewer.author_count == 0:
        return ''

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.author_count} published reviews."


# print(get_top_reviewer())


def get_latest_article():
    latest_article = Article.objects.prefetch_related('authors').order_by('published_on').first()

    if latest_article is None:
        return ''

    all_authors = latest_article.authors.all().order_by('full_name')
    authors = ", ".join(author.full_name for author in all_authors)

    reviews= Review.objects.filter(article=latest_article).aggregate(num_reviews = Count('id'),avg_rating=Avg('rating'))
    return (f"The latest article is: {latest_article.title}. Authors: {authors}. "
            f"Reviewed: {reviews['num_reviews']} times. Average Rating: {reviews['avg_rating']}.")

# print(get_latest_article())

def get_top_rated_article():
    top_rated_articles = (Article.objects.annotate(num_reviews =Count('review'),avg_rating=Avg('review__rating')).filter(num_reviews__gt=0).order_by('-num_reviews','title'))
    top_article =top_rated_articles.first()
    if top_article is None:
        return ''
    return f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, reviewed {top_article.num_reviews} times."

# print(get_top_rated_article())

def ban_author(email=None):
    if email is None:
        return "No authors banned."
    author_to_ban = Author.objects.filter(email=email).first()


    if author_to_ban is None:
        return "No authors banned."

    num_reviews = Review.objects.filter(author=author_to_ban).count()
    if num_reviews == 0:
        return "No authors banned."
    Review.objects.filter(author = author_to_ban ).delete()
    author_to_ban.is_banned = True
    author_to_ban.save()
    return f"Author: {author_to_ban.full_name} is banned! {num_reviews} reviews deleted."


# print(ban_author(email='alice@mail.com'))

#extra practice
def get_review_with_author_info_and_article_title():
    reviews = Review.objects.select_related('author', 'article').all()
    final_line = []

    for r in reviews:
        final_line.append(f'The author name is: {r.author.full_name} '
                          f'\nThe article title is: {r.article.title} '
                          f'\nThe content is: {r.content}')

    return '\n'.join(final_line)

# print(get_review_with_author_info_and_article_title())

def get_all_articles_with_authors_info():
    articles = Article.objects.prefetch_related('authors').all()

    final_line = []
    for article in articles:
        final_line.append(f'The article is: {article.title} ')
        for author in article.authors.all():
            final_line.append(f'-The author is: {author.full_name} ')

    return '\n'.join(final_line)

# print(get_all_Articles_with_authorsinfo())
