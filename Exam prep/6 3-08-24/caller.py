import os
import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from datetime import date, datetime

from main_app.models import Astronaut, Spacecraft, Mission
# Create queries within functions

def populate_db():
    # -----------------------
    # ASTRONAUTS
    # -----------------------

    john = Astronaut.objects.create(
        name="John Deer",
        phone_number="853967",
        is_active=True,
        date_of_birth=date(1980, 1, 1),
        spacewalks=3,
    )

    jane = Astronaut.objects.create(
        name="Jane Smith",
        phone_number="123456",
        is_active=True,
        date_of_birth=date(1985, 5, 15),
        spacewalks=1,
    )

    josie = Astronaut.objects.create(
        name="Josie Stam",
        phone_number="111111",
        is_active=False,
        date_of_birth=date(1990, 3, 12),
        spacewalks=0,
    )

    # -----------------------
    # SPACECRAFTS
    # -----------------------

    explorer1 = Spacecraft.objects.create(
        name="Explorer I",
        manufacturer="SpaceTech Inc.",
        capacity=5,
        weight=12000.5,
        launch_date=datetime(2022, 1, 1, 0, 0),
    )

    explorer2 = Spacecraft.objects.create(
        name="Explorer II",
        manufacturer="SpaceX",
        capacity=2,
        weight=10000.2,
        launch_date=datetime(2023, 5, 1, 0, 0),
    )

    # -----------------------
    # MISSIONS
    # -----------------------

    mission1 = Mission.objects.create(
        name="Moon Landing",
        description="Landing on the moon",
        status=Mission.StatusChoices.PLANNED,
        launch_date=datetime(2024, 10, 10, 0, 0),
        spacecraft=explorer1,
        commander=john,
    )
    mission1.astronauts.set([john, jane])

    mission2 = Mission.objects.create(
        name="Moon Landing2",
        description="Landing on the moon",
        status=Mission.StatusChoices.COMPLETED,
        launch_date=datetime(2024, 3, 1, 0, 0),
        spacecraft=explorer1,
        commander=josie,
    )
    mission2.astronauts.set([jane, josie])

    print("Database populated successfully!")

# populate_db()

def get_astronauts(search_string=None):
    if search_string is None:
        return ''
    astronaut_name = Q(name__icontains=search_string)
    astronaut_phone_number = Q(phone_number__icontains=search_string)

    if astronaut_name is not None or astronaut_phone_number is not None:
        query = astronaut_name | astronaut_phone_number
    elif astronaut_name is not None:
        query = astronaut_name
    else:
        query = astronaut_phone_number

    astronaut = Astronaut.objects.filter(query).order_by('name')

    final_text = []
    for a in astronaut:
        final_text.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}")

    return '\n'.join(final_text)

# print(get_astronauts(search_string='jO'))
# print(get_astronauts(search_string='zzz'))

def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()
    if astronaut is None:
        return 'No data.'

    return f"Top Astronaut: {astronaut.name} with {astronaut.astronauts_count} missions."

# print(get_top_astronaut())
# Top Astronaut: Jane Smith with 2 missions.
def get_top_commander():
    astronaut = Astronaut.objects.annotate(count_commander_missions = Count('missions_commander')).order_by('-count_commander_missions','phone_number').first()
    if astronaut is None or astronaut.count_commander_missions == 0:
        return 'No data.'
    return f"Top Commander: {astronaut.name} with {astronaut.count_commander_missions} commanded missions."
# print(get_top_commander())
# Top Commander: Josie Stam with 1 commanded missions. (/)

def get_last_completed_mission():
    last_mission = Mission.objects.filter(status= Mission.StatusChoices.COMPLETED).order_by('-launch_date').first()
    if last_mission is None:
        return 'No data.'

    all_astronauts = last_mission.astronauts.all().order_by('name')
    astronauts = ', '.join(a.name for a in all_astronauts)

    spacewalks = Astronaut.objects.filter(missions_astronauts=last_mission).aggregate(total_spacewalks=Sum('spacewalks'))
    return (f"The last completed mission is: {last_mission.name}. "
            f"Commander: {'TBA' if last_mission.commander is None else last_mission.commander.name}. "
            f"Astronauts: {astronauts}. "
            f"Spacecraft: {last_mission.spacecraft.name}. "
            f"Total spacewalks: {spacewalks['total_spacewalks']}.")
print(get_last_completed_mission())
# The last completed mission is: Moon Landing2. Commander: Josie Stam. Astronauts: Jane Smith, Josie Stam. Spacecraft: Explorer I. Total spacewalks: 1


def get_most_used_spacecraft():
    # o	The 'astronauts on missions' represent the number of unique astronauts who have been on missions with this spacecraft.
    spacecraft = Spacecraft.objects.annotate(total_missions = Count('missions_spacecraft',distinct=True),count_astronauts = Count('missions_spacecraft__astronauts',distinct=True)).order_by('-total_missions','name').first()
    if spacecraft is None:
        return 'No data.'

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.total_missions} missions, "
            f"astronauts on missions: {spacecraft.count_astronauts}.")

print(get_most_used_spacecraft())
# The most used spacecraft is: Explorer I, manufactured by SpaceTech Inc., used in 2 missions, astronauts on missions: 3.
def decrease_spacecrafts_weight():
    spacecraft = Spacecraft.objects.filter(missions_spacecraft__status= Mission.StatusChoices.PLANNED,weight__gt=200.0)
    if not spacecraft:
        return "No changes in weight."
    num_of_spacecrafts_affected = spacecraft.count()
    spacecraft.update(weight= F('weight') -200.0)


    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']
    return f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"
print(decrease_spacecrafts_weight())
# The weight of 1 spacecrafts has been decreased. The new average weight of all spacecrafts is 10900.4kg
