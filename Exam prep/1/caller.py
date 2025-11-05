import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# # Import your models here
from main_app.models import Actor, Director,Movie
#2
# # Create queries within functions
#
# def populate_db():
#     director1 = Director.objects.create(
#         full_name='Viki t',
#         birth_date='1997-06-06',
#         nationality='Bulgaria',
#         years_of_experience=5,
#     )
#
#     director2 = Director.objects.create(
#         full_name='Niki E',
#         birth_date='1998-06-12',
#         nationality='Bulgaria',
#         years_of_experience=10,
#     )
#     director3 = Director.objects.create(
#         full_name='Ruji B',
#         birth_date='2000-01-15',
#         nationality='Bulgaria',
#         years_of_experience=2,
#     )
#
#     actor1 = Actor.objects.create(
#         full_name='Viki S',
#         birth_date='1997-06-06',
#         nationality='Bulgaria',
#         is_awarded=True,
#     )
#     actor2 = Actor.objects.create(
#         full_name='Niki M',
#         birth_date='1999-09-06',
#         nationality='Bulgaria',
#         is_awarded=False,
#     )
#     actor3 = Actor.objects.create(
#         full_name='Ruji E',
#         birth_date='1991-06-10',
#         nationality='Bulgaria',
#         is_awarded=True,
#     )
#     movie1 = Movie.objects.create(
#         title = 'Mystery',
#         release_date='2001-01-01',
#         storyline='Very cute drama',
#         genre='Drama',
#         rating=5.3,
#         is_classic=True,
#         director=director1,
#         starring_actor=actor1,
#
#     )
#     movie1.actors.add(actor2,actor3)
#
#     movie2 = Movie.objects.create(
#         title='Sexy Movie',
#         release_date='2023-01-01',
#         storyline='Very sexy Action',
#         genre='Action',
#         rating=8.5,
#         is_classic=False,
#         director=director2,
#         starring_actor=actor2,
#
#     )
#     movie2.actors.add(actor1, actor3)
#
#     movie3 = Movie.objects.create(
#         title='Another boring movie',
#         release_date='2025-01-01',
#         storyline='Very funny comedy',
#         genre='Comedy',
#         rating=8.2,
#         is_classic=False,
#         director=director3,
#         starring_actor=actor3,
#     )
#     movie3.actors.add(actor1, actor2)

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)
    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query= query_name
    else:
        query = query_nationality

    directors= Director.objects.filter(query).order_by('full_name')
    if not directors:
        return ''
    result = []
    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.experience}")
    return '\n'.join(result)

def get_top_director():
    director= Director.objects.get_directors_by_movies_count().first()
    if director is None:
        return ''
    return f"Top Director: {director.full_name}, movies: {director.movies_count}."

def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies').annotate(
        movies_count=Count('starring_movies'),
        avg_rating=Avg('starring_movies__rating')).order_by('-movies_count','full_name').first()

    if not actor or not actor.movies_count:
        return ''

    movies = ', '.join(m.title for m in actor.starring_movies.all())
    return (f"Top Actor: {actor.full_name}, starring in movies: {movies}."
            f" movies average rating: {actor.avg_rating:.1f}")

#"Top Actor: {actor_full_name}, starring in movies: {movie_title1}, {movie_title2}, … {movie_titleN}, movies average rating: {movies_avg_rating}"



def get_actors_by_movies_count():
    actors = Actor.objects.annotate(movies_count=Count('actor_movies')).order_by('movies_count','full_name')[:3]

    if not actors or not actors[0].movies_count:
        return ''

    result = []
    for a in actors:
        result.append(f"{a.full_name1}, participated in {a.movies_count} movies")
    return '\n'.join(result)



def get_top_rated_awarded_movie():
    top_movie = (Movie.objects.select_related('starring_actor')
                 .prefetch_related('actors')
                 .filter(is_rated=True)
                 .order_by('-rating','title')
                 .first())
    if top_movie is None:
        return ''
    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    participationg_actors = top_movie.actors.order_by('full_name').values_list(
        'full_name',flat=True )

    cast =', '.join(participationg_actors)
    return (f"Top rated awarded movie: {top_movie.title}, "
            f"rating: {top_movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. "
            f"Cast: {cast}.")
#Return a string in the following format:
# "Top rated awarded movie: {movie_title}, rating: {movie_rating}.
# Starring actor: {starring_actor_full_name/'N/A'}. Cast: {participating_actor1}, {participating_actor2}, …{participating_actorN}."
def increase_rating():
    movies_to_update= Movie.objects.filter(is_classic=True,rating__lt=10)
    if not movies_to_update:
        return "No ratings increased."
    updated_movies_count = movies_to_update.count()
    movies_to_update.update(rating= F('rating')+ 0.1)

    return f"Rating increased for {updated_movies_count} movies."
#"Rating increased for {num_of_updated_movies} movies."

print(Director.objects.get_directors_by_movies_count())