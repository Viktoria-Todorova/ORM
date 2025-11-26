import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# from datetime import date, timezone, datetime
from main_app.models import Quest, Dragon, House
from django.db.models import Q, F, Min, Avg


# Create queries within functions
# def populate_db():
#     # -----------------------------
#     # HOUSES
#     # -----------------------------
#     stark = House.objects.create(
#         name="House Stark",
#         motto="Winter is Coming",
#         castle="Winterfell",
#         is_ruling=False,
#         wins=3,
#     )
#
#     targaryen = House.objects.create(
#         name="House Targaryen",
#         motto="Fire and Blood",
#         castle="Dragonstone",
#         is_ruling=True,
#         wins=5,
#     )
#
#     lannister = House.objects.create(
#         name="House Lannister",
#         motto="Hear Me Roar",
#         castle="Casterly Rock",
#         is_ruling=False,
#         wins=2,
#     )
#
#     enemy = House.objects.create(
#         name="House Enemy",
#         motto="Starks are Down",
#         castle=None,
#         is_ruling=False,
#         wins=0,
#     )
#
#     # -----------------------------
#     # DRAGONS
#     # -----------------------------
#     drogon = Dragon.objects.create(
#         name="Drogon",
#         power=9.9,
#         breath=Dragon.BreathChoices.FIRE,
#         is_healthy=True,
#         birth_date=date(2020, 5, 17),
#         wins=5,
#         house=targaryen
#     )
#
#     rhaegal = Dragon.objects.create(
#         name="Rhaegal",
#         power=8.6,
#         breath=Dragon.BreathChoices.FIRE,
#         is_healthy=True,
#         birth_date=date(2020, 5, 17),
#         wins=3,
#         house=targaryen
#     )
#
#     viserion = Dragon.objects.create(
#         name="Viserion",
#         power=1.2,
#         breath=Dragon.BreathChoices.FIRE,
#         is_healthy=False,
#         birth_date=date(2020, 5, 17),
#         wins=2,
#         house=targaryen
#     )
#
#     syrax = Dragon.objects.create(
#         name="Syrax",
#         power=8.0,
#         breath=Dragon.BreathChoices.FIRE,
#         is_healthy=True,
#         birth_date=date(2021, 5, 17),
#         wins=1,
#         house=targaryen
#     )
#
#     silverwing = Dragon.objects.create(
#         name="Silverwing",
#         power=7.5,
#         breath=Dragon.BreathChoices.ICE,
#         is_healthy=True,
#         birth_date=date(2021, 6, 17),
#         wins=1,
#         house=stark
#     )
#
#     shrykos = Dragon.objects.create(
#         name="Shrykos",
#         power=7.8,
#         breath=Dragon.BreathChoices.LIGHTNING,
#         is_healthy=True,
#         birth_date=date(2021, 7, 17),
#         wins=2,
#         house=stark
#     )
#
#     vermax = Dragon.objects.create(
#         name="Vermax",
#         power=7.8,
#         breath=Dragon.BreathChoices.FIRE,
#         is_healthy=True,
#         birth_date=date(2021, 8, 17),
#         wins=1,
#         house=lannister
#     )
#
#     # -----------------------------
#     # QUESTS
#     # -----------------------------
#     # 1. Battle of Winterfell
#     bow = Quest.objects.create(
#         name="Battle of Winterfell",
#         code="BoW#",
#         reward=500.0,
#         start_time=datetime(2023, 12, 1, 12, 0, tzinfo=timezone.utc),
#         host=stark
#     )
#     bow.dragons.set([shrykos, silverwing])
#
#     # 2. Siege of Meereen
#     som = Quest.objects.create(
#         name="Siege of Meereen",
#         code="SoM#",
#         reward=1000.0,
#         start_time=datetime(2024, 6, 24, 12, 0, tzinfo=timezone.utc),
#         host=targaryen
#     )
#     som.dragons.set([drogon, rhaegal, viserion])
#
#     # 3. Battle of Blackwater
#     bob = Quest.objects.create(
#         name="Battle of Blackwater",
#         code="BoB#",
#         reward=700.0,
#         start_time=datetime(2024, 8, 1, 12, 0, tzinfo=timezone.utc),
#         host=lannister
#     )
#     bob.dragons.set([drogon, vermax])
#
#     print("Database populated successfully!")
#


def get_houses(search_string=None):
    if not search_string:
        return "No houses match your search."

    # name = Q(name__istartswith=search_string)
    #
    # motto = Q(motto__istartswith=search_string)
    #
    # if name is not None or motto is not None:
    #     query = name | motto
    # elif name is not None:
    #     query = name
    # else:
    #     query = motto

    query = Q(name__istartswith=search_string) | Q(motto__istartswith=search_string)

    matched_houses = House.objects.filter(query).order_by('-wins','name')

    if not matched_houses.exists():
        return "No houses match your search."
    final_text =[]
    for h in matched_houses:
        motto = h.motto if h.motto else "N/A"
        final_text.append(f'House: {h.name}, wins: {h.wins}, motto: {motto}')
    return '\n'.join(final_text)

# print(get_houses("star"))
# House: Stark, wins: 3, motto: Winter is Coming
# House: Enemy, wins: 0, motto: Starks are Down
# print(get_houses("Roar"))
# No houses match your search.
def get_most_dangerous_house():
    most_dangerous_house = House.objects.get_houses_by_dragons_count().first()
    if most_dangerous_house is None or most_dangerous_house.num_dragons == 0:
        return "No relevant data."

    return (f'The most dangerous house is the House of {most_dangerous_house.name} with {most_dangerous_house.num_dragons} dragons. '
            f'Currently {"ruling" if most_dangerous_house.is_ruling else "not ruling"} the kingdom.')
# print(get_most_dangerous_house())
# The most dangerous house is the House of Targaryen with 4 dragons. Currently ruling the kingdom.
def get_most_powerful_dragon():
    dragon = Dragon.objects.filter(is_healthy=True).order_by('-power','name').first()
    if dragon is None or dragon.is_healthy is False:
        return "No relevant data."
    num_quests = dragon.quests.count()
    return (f"The most powerful healthy dragon is {dragon.name} with a power level of {dragon.power:.1f}, "
            f"breath type {dragon.breath}, and {dragon.wins} wins, "
            f"coming from the house of {dragon.house.name}. "
            f"Currently participating in {num_quests} quests.")

# print(get_most_powerful_dragon())
# The most powerful healthy dragon is Drogon with a power level of 9.9, breath type Fire, and 5 wins, coming from the house of Targaryen. Currently participating in 2 quests.





def update_dragons_data():
    injured_dragon = Dragon.objects.filter(is_healthy=False,power__gt=1.0)
    if not injured_dragon.exists():
        return "No changes in dragons data."
    # injured_dragon.update(power=F('power') - 0.1, is_healthy=True)

    for dragon in injured_dragon:
        dragon.power = F('power') -0.1
        dragon.is_healthy = True
        dragon.save()

    num_of_dragons_affected =injured_dragon.count()
    min_power = Dragon.objects.aggregate(Min('power'))['power__min']

    return f"The data for {num_of_dragons_affected} dragon/s has been changed. The minimum power level among all dragons is {min_power:.1f}"
# print(update_dragons_data())
# The data for 1 dragon/s has been changed. The minimum power level among all dragons is 1.1
def get_earliest_quest():
    quest = Quest.objects.order_by('start_time').first()
    if not quest:
        return "No relevant data."
    date = quest.start_time
    dragons =quest.dragons.all().order_by('-power','name')
    dragons_name = '*'.join(d.name for d in dragons)
    avg_power = dragons.aggregate(avg_power_level = Avg('power'))['avg_power_level'] #or 0
    return (f'The earliest quest is: {quest.name}, '
            f'code: {quest.code}, '
            f'start date: {date.day}.{date.month}.{date.year}, '
            f'host: {quest.host.name}. '
            f'Dragons: {dragons_name}. '
            f'Average dragons power level: {avg_power:.2f}')
# print(get_earliest_quest())
# The earliest quest is: Battle of Winterfell, code: BoW#, start date: 1.12.2023, host: Stark. Dragons: Shrykos*Silverwing. Average dragons power level: 7.65
def announce_quest_winner(quest_code):


    quest = Quest.objects.filter(code=quest_code).first()
    if not quest:
        return "No such quest."
    quest_name = quest.name
    quest_reward = quest.reward
    most_powerful_dragon = quest.dragons.filter(is_healthy=True).order_by('-power','name').first()
    most_powerful_dragon.wins += 1
    most_powerful_dragon.house.wins += 1
    most_powerful_dragon.save()
    most_powerful_dragon.house.save()
    quest.delete()


    return (f'The quest: {quest_name} has been won by dragon {most_powerful_dragon.name} from house {most_powerful_dragon.house.name}. '
            f'The number of wins has been updated as follows: {most_powerful_dragon.wins} '
            f'total wins for the dragon and {most_powerful_dragon.house.wins} total wins for the house. '
            f'The house was awarded with {quest_reward:.2f} coins.')
# print(announce_quest_winner('W#'))
# No such quest.
# print(announce_quest_winner('SoM#'))
# The quest: Battle of Winterfell has been won by dragon Shrykos from house Stark. The number of wins has been updated as follows: 3 total wins for the dragon and 4 total wins for the house. The house was awarded with 500.00 coins.




# print(House.objects.get_houses_by_dragons_count())
# <QuerySet [<House: Targaryen>, <House: Stark>, <House: Lannister>, <House: Enemy>]>





