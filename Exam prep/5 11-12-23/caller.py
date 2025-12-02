import os


import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from datetime import date, datetime
from main_app.models import TennisPlayer, Tournament, Match
# Create queries within functions
from datetime import datetime, date
from django.utils import timezone


# Function to populate the database
def populate_database():
    """
    Populates the database with sample tennis data.
    """


    # Create Tennis Players
    p1 = TennisPlayer.objects.create(full_name="Rafael Nadal", birth_date=date(1986, 6, 3), country="Spain", ranking=2,
                                     is_active=True)
    p2 = TennisPlayer.objects.create(full_name="Novak Djokovic", birth_date=date(1987, 5, 22), country="Serbia",
                                     ranking=1, is_active=True)
    p3 = TennisPlayer.objects.create(full_name="Roger Federer", birth_date=date(1981, 8, 8), country="Switzerland",
                                     ranking=15, is_active=False)
    p4 = TennisPlayer.objects.create(full_name="Carlos Alcaraz", birth_date=date(2003, 5, 5), country="Spain",
                                     ranking=3, is_active=True)
    p5 = TennisPlayer.objects.create(full_name="Daniil Medvedev", birth_date=date(1996, 2, 11), country="Russia",
                                     ranking=4, is_active=True)
    p6 = TennisPlayer.objects.create(full_name="Jannik Sinner", birth_date=date(2001, 8, 16), country="Italy",
                                     ranking=5, is_active=True)
    p7 = TennisPlayer.objects.create(full_name="Stefanos Tsitsipas", birth_date=date(1998, 8, 12), country="Greece",
                                     ranking=6, is_active=True)
    p8 = TennisPlayer.objects.create(full_name="Alexander Zverev", birth_date=date(1997, 4, 20), country="Germany",
                                     ranking=7, is_active=True)

    print("✓ Created 8 Tennis Players")

    # Create Tournaments
    t1 = Tournament.objects.create(name="Australian Open 2024", location="Melbourne", prize_money=86500000.00,
                                   start_date=date(2024, 1, 14), surface_type="Hard Court")
    t2 = Tournament.objects.create(name="French Open 2024", location="Paris", prize_money=53478000.00,
                                   start_date=date(2024, 5, 26), surface_type="Clay")
    t3 = Tournament.objects.create(name="Wimbledon 2024", location="London", prize_money=50000000.00,
                                   start_date=date(2024, 7, 1), surface_type="Grass")
    t4 = Tournament.objects.create(name="US Open 2024", location="New York", prize_money=65000000.00,
                                   start_date=date(2024, 8, 26), surface_type="Hard Court")
    t5 = Tournament.objects.create(name="Madrid Open 2024", location="Madrid", prize_money=8564465.00,
                                   start_date=date(2024, 4, 24), surface_type="Clay")
    t6 = Tournament.objects.create(name="Miami Open 2024", location="Miami", prize_money=8800000.00,
                                   start_date=date(2024, 3, 19), surface_type="Hard Court")

    print("✓ Created 6 Tournaments")

    # Create Matches
    m1 = Match.objects.create(
        score="6-4, 7-6(3), 6-3",
        summary="Intense final match with incredible baseline rallies and strategic gameplay throughout.",
        date_played=timezone.make_aware(datetime(2024, 1, 28, 19, 30)),
        tournament=t1,
        winner=p6
    )
    m1.players.add(p2, p6)

    m2 = Match.objects.create(
        score="6-3, 7-6(5), 6-3",
        summary="Dominant performance on clay court with powerful forehands and defensive mastery.",
        date_played=timezone.make_aware(datetime(2024, 6, 9, 15, 0)),
        tournament=t2,
        winner=p4
    )
    m2.players.add(p1, p4)

    m3 = Match.objects.create(
        score="7-6(4), 6-4, 6-7(3), 6-3",
        summary="Classic grass court tennis with excellent serve and volley play from both competitors.",
        date_played=timezone.make_aware(datetime(2024, 7, 14, 14, 0)),
        tournament=t3,
        winner=p4
    )
    m3.players.add(p4, p2)

    m4 = Match.objects.create(
        score="6-4, 6-4, 6-2",
        summary="Powerful serving and aggressive baseline play dominated this hard court showdown.",
        date_played=timezone.make_aware(datetime(2024, 9, 8, 16, 0)),
        tournament=t4,
        winner=p6
    )
    m4.players.add(p6, p5)

    m5 = Match.objects.create(
        score="7-5, 6-4",
        summary="Exciting semi-final with multiple break points and thrilling tiebreaks.",
        date_played=timezone.make_aware(datetime(2024, 5, 3, 18, 30)),
        tournament=t5,
        winner=p8
    )
    m5.players.add(p7, p8)

    m6 = Match.objects.create(
        score="6-7(5), 7-6(7), 7-6(4)",
        summary="Marathon match lasting over three hours with incredible mental fortitude displayed.",
        date_played=timezone.make_aware(datetime(2024, 3, 31, 13, 0)),
        tournament=t6,
        winner=p6
    )
    m6.players.add(p5, p6)

    m7 = Match.objects.create(
        score="6-2, 6-3",
        summary="Quick and decisive victory with excellent court coverage and shot placement.",
        date_played=timezone.make_aware(datetime(2024, 1, 26, 19, 0)),
        tournament=t1,
        winner=p2
    )
    m7.players.add(p2, p4)

    m8 = Match.objects.create(
        score="4-6, 6-3, 6-7(4), 7-6(8), 6-2",
        summary="Epic five-set battle showcasing stamina and determination from both players.",
        date_played=timezone.make_aware(datetime(2024, 6, 7, 11, 0)),
        tournament=t2,
        winner=p1
    )
    m8.players.add(p1, p2)

    print("✓ Created 8 Matches")
    print("\n" + "=" * 50)
    print("DATABASE POPULATION COMPLETE!")
    print("=" * 50)
    print(f"Tennis Players: {TennisPlayer.objects.count()}")
    print(f"Tournaments: {Tournament.objects.count()}")
    print(f"Matches: {Match.objects.count()}")
    print("=" * 50)


def clear_database():
    """
    Clears all tennis data from the database.
    """


    Match.objects.all().delete()
    Tournament.objects.all().delete()
    TennisPlayer.objects.all().delete()

    print("✓ All tennis data has been cleared from the database.")


# if __name__ == "__main__":
#     # clear_database()
#     populate_database()


#4
def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''
    name = Q(full_name__icontains=search_name)
    country = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        query = name | country
    elif search_name is not None:
        query = name
    else:
        query = country

    player = TennisPlayer.objects.filter(query).order_by('ranking')
    if not player:
        return ''

    return '\n'.join(f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}" for p in player)

# print(get_tennis_players('Rafael Nadal','Spain'))

def get_top_tennis_player():
    top_player= TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins} wins." if top_player else ""

# print(get_top_tennis_player())

def get_tennis_player_by_matches_count():
    player = (TennisPlayer.objects.annotate(matches_count = Count('matches')).
              order_by('-matches_count','ranking' )).first()
    if player is None or player.matches_count == 0:
        return ''
    return f"Tennis Player: {player.full_name} with {player.matches_count} matches played."

# print(get_tennis_player_by_matches_count())


#5

def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''
    tournament = Tournament.objects.filter(surface_type=surface).all()

    if tournament is None:
        return ''

    ordered_tournaments = tournament.order_by('-start_date')
    final_text = []
    for t in ordered_tournaments:
        num_matches = Match.objects.filter(tournament=t).count()
        final_text.append(f"Tournament: {t.name}, start date: {t.start_date}, matches: {num_matches}")

    return '\n'.join(final_text)
# print(get_tournaments_by_surface_type('Clay'))

def get_latest_match_info():
    latest_match = Match.objects.prefetch_related('players', 'tournament').order_by('-date_played').first()
    if latest_match is None:
        return ''
    all_players = latest_match.players.order_by('full_name')
    players =  ' vs '.join(l.full_name for l in all_players)#latest_match.players
    winner = latest_match.winner.full_name if latest_match.winner is not None else "TBA"
    return (f"Latest match played on: {latest_match.date_played}, "
            f"tournament: {latest_match.tournament.name}, "
            f"score: {latest_match.score}, "
            f"players: {players}, "
            f"winner: {winner}, "
            f"summary: {latest_match.summary}")

# print(get_latest_match_info())
def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.filter(tournament__name=tournament_name).order_by('-date_played')

    if not matches:
        return "No matches found."
    final_text = []
    for m in matches:
        final_text.append(f'Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner is not None else "TBA"}')

    return '\n'.join(final_text)
# print(get_matches_by_tournament('Australian Open 2024'))
