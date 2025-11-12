import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Movie, Actor, Director
from django.db.models import Q, Count, Avg, F


# Create queries within functions

def populate_db():
    director1 = Director.objects.create(
        full_name='Viki t',
        birth_date='1997-06-06',
        nationality='Bulgaria',
        years_of_experience=5,
    )

    director2 = Director.objects.create(
        full_name='Niki E',
        birth_date='1998-06-12',
        nationality='Bulgaria',
        years_of_experience=10,
    )
    director3 = Director.objects.create(
        full_name='Ruji B',
        birth_date='2000-01-15',
        nationality='Bulgaria',
        years_of_experience=2,
    )

    actor1 = Actor.objects.create(
        full_name='Viki S',
        birth_date='1997-06-06',
        nationality='Bulgaria',
        is_awarded=True,
    )
    actor2 = Actor.objects.create(
        full_name='Niki M',
        birth_date='1999-09-06',
        nationality='Bulgaria',
        is_awarded=False,
    )
    actor3 = Actor.objects.create(
        full_name='Ruji E',
        birth_date='1991-06-10',
        nationality='Bulgaria',
        is_awarded=True,
    )
    movie1 = Movie.objects.create(
        title='Mystery',
        release_date='2001-01-01',
        storyline='Very cute drama',
        genre='Drama',
        rating=5.3,
        is_classic=True,
        director=director1,
        starring_actor=actor1,

    )
    movie1.actors.add(actor2, actor3)

    movie2 = Movie.objects.create(
        title='Sexy Movie',
        release_date='2023-01-01',
        storyline='Very sexy Action',
        genre='Action',
        rating=8.5,
        is_classic=False,
        director=director2,
        starring_actor=actor2,

    )
    movie2.actors.add(actor1, actor3)

    movie3 = Movie.objects.create(
        title='Another boring movie',
        release_date='2025-01-01',
        storyline='Very funny comedy',
        genre='Comedy',
        rating=8.2,
        is_classic=False,
        director=director3,
        starring_actor=actor3,
    )
    movie3.actors.add(actor1, actor2)




def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name) #todo
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality

    #perform Query

    directors = Director.objects.filter(query).order_by('full_name')

    final_line = []
    for d in directors:
        final_line.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}")


    return '\n'.join(final_line)

#print(get_directors(search_name='V', search_nationality=None))
# print(get_directors(search_name='Martin', search_nationality='Canadian'))


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if director is None:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.movie_count}."

#print(get_top_director())

def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies').annotate(
        movie_count=Count('starring_movies'),
        avg_rating=Avg('starring_movies__rating'),
    ).order_by('-movie_count','full_name').first()

    if actor is None:
        return ''

    movies = []

    for m in actor.starring_movies.all():
        movies.append(m.title)

    return f"Top Actor: {actor.full_name}, starring in movies: {', '.join(movies)}, movies average rating: {actor.avg_rating:.1f}"

#print(get_top_actor())

def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        movie_count=Count('actors_movies')
    ).order_by(
        '-movie_count','full_name' )[:3]

    if len(actors) == 0:
        return ''

    return '\n'.join(f"{a.full_name}, participated in {a.movie_count} movies" for a in actors)

# print(get_actors_by_movies_count())

def get_top_rated_awarded_movie():
    awarded_movie = (Movie.objects.select_related('starring_actor').
                     prefetch_related('actors').
                     filter(is_awarded=True).
                     order_by('-rating','title').
                     first())

    if awarded_movie is None:
        return ''
    starring_actor = awarded_movie.starring_actor.full_name if awarded_movie.starring_actor else 'N/A'

    # Get all actors' full names sorted alphabetically
    cast = sorted(actor.full_name for actor in awarded_movie.actors.all())


    return (f"Top rated awarded movie: {awarded_movie.title}, "
            f"rating: {awarded_movie.rating:.1f}. "
                f"Starring actor: {starring_actor}. "
                f"Cast: {', '.join(cast)}.")

#print(get_top_rated_awarded_movie())

def increase_rating():
    movies_to_increase = Movie.objects.filter(is_classic=True,rating__lt = 10)

    if not movies_to_increase:
        return "No ratings increased."

    num_of_updated_movies = movies_to_increase.count()
    movies_to_increase.update(rating = F('rating') + 0.1)
    return f"Rating increased for {num_of_updated_movies} movies."

#print(increase_rating())