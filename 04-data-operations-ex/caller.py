import os


import django
from django.db.models import QuerySet, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from orm_skeleton.choices import RoomTypeChoices, CharactersChoices
#from populate_db import populate_model_with_data
from main_app.models import Car, Task, HotelRoom, Character, Pet, Artifact, Location
from decimal import Decimal
from django.db.models import QuerySet
# Create queries within functions

#1
def create_pet(name: str, species: str) -> str:
    pet = Pet(name=name, species=species)
    pet.save()

    return f"{name} is a very cute {species}!"

#2

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool)->str:
    artifact = Artifact(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    artifact.save()
    return f"The artifact {name} is {age} years old!"

def rename_artifact(artifact: Artifact, new_name: str) ->None:
    if artifact.is_magical and artifact.age >250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()

#3

def show_all_locations() ->str:
    locations = Location.objects.all().order_by("-id")
    return "\n".join(f"{loc.name} has a population of {loc.population}!" for loc in locations)

def new_capital() ->None:
    first_location = Location.objects.first()
    first_location.is_capital =True
    first_location.save()

def get_capitals() ->QuerySet[Location]:
    return Location.objects.filter(is_capital=True).values('name')

def delete_first_location()->None:
    Location.objects.first().delete()

#4
def apply_discount() -> None:
    cars=Car.objects.all()
    updated_cars = []
    for car in cars:
        percentage_off = Decimal(str(sum(int(digit) for digit in str(car.year))/100))
        #car.year = "2018"> 2 > 2+0 > 2+0+1 > 2+0+1+9 > 11 /100 > 0.11
        discount = car.price * percentage_off
        car.price_with_discount = car.price -discount
        #car.save()
        updated_cars.append(car)
    Car.objects.bulk_update(updated_cars,['price_with_discount'])


def get_recent_cars() ->QuerySet[dict]:
    """"
    SELECT model,price FROM cars Where year >2020
    """

    return Car.objects.filter(year__gt= 2020).values('model','price')

def delete_last_car()-> None:
    Car.objects.last().delete()



#apply_discount()
#print(get_recent_cars())


#5 Task Encoder

def show_unfinished_tasks() -> str:
    tasks = Task.objects.filter(is_finished=False)
    return "\n".join(f"Task - {t.title} needs to be done until {t.due_date}!" for t in tasks)

#populate_model_with_data(Task)
#print(show_unfinished_tasks())

def complete_odd_tasks() -> None:
    #1st option
    # for task in Task.objects.all():
    #     if task.id % 2 == 1:
    #         task.is_finished = True
    #         task.save()

    #2nd option- more optimized
    tasks= Task.objects.all()
    completed_tasks = []
    for task in tasks:
        if task.id % 2 == 1:
            task.is_finished = True
            completed_tasks.append(task)
    Task.objects.bulk_update(completed_tasks,['is_finished'])


#complete_odd_tasks()


# encodes the text and replaces it with the description for all tasks with the given title.
# The encoded text should be 3 ASCII symbols below the given one.
def encode_and_replace(text: str, task_title: str):

    encoded_text =''.join(chr(ord(c) -3)for c in text)
    # 1st option
    # for task in Task.objects.filter(title=task_title):
    #     task.description = encoded_text
    #     task.save()

    #2nd option- optimized
    # """
    #     UPDATE tasks
    #     SET description = encoded_text
    #     WHERE title= task_title
    # """
    Task.objects.filter(title=task_title).update(description=encoded_text)


#6.	Hotel Room

def get_deluxe_rooms() ->str:
    deluxe_room = HotelRoom.objects.filter(room_type= RoomTypeChoices.DELUXE)
    even_id_deluxe_rooms = []
    for room in deluxe_room:
        if room.id%2 == 0:
            even_id_deluxe_rooms.append(room.id)
    return "\n".join(
        f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!"
        for r in even_id_deluxe_rooms
    )
#populate_model_with_data(HotelRoom)

def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')
    previous_room: HotelRoom = None

    # •	If the room is not reserved, proceed to the next one.
    # •	If the first room in the database is reserved (there is no previous room):
    # o	Increase the capacity with its id number.
    for room in rooms:
        if not room.is_reserved:
            continue
        if previous_room:
            room.capacity += previous_room.capacity
        else:
            room.capacity += room.id
        previous_room = room
        room.save()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room()-> None:
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        last_room.delete()

#7

class CharacterTypeChoices:
    pass


def update_characters() -> None:
    """
    UPDATE CHARACTERS
    SET level =level+3,intelligence =inteligence -7
    WHERE class_name = 'Mage'
    """

    #•	If the class name is "Mage" - increase the level by 3 and decrease the intelligence by 7.
    # •	If the class name is "Warrior" - decrease the hit points by half and increase the dexterity by 4.
    # •	If the class name is "Assassin" or "Scout" - update their inventory to "The inventory is empty".

    Character.objects.filter(class_name=CharactersChoices.MAGE).update(
        level=F('level')+3,
        intelligence=F('intelligence')-7,
    )
    Character.objects.filter(class_name=CharactersChoices.WARRIOR).update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )

    Character.objects.filter(class_name__in=[CharactersChoices.SCOUT,CharactersChoices.ASSASSIN]).update(
        inventory= f"The inventory is empty"
    )

#update_characters()

def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_inventory =None
    if first_character.class_name in [ CharactersChoices.MAGE, CharactersChoices.SCOUT]:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [CharactersChoices.WARRIOR, CharactersChoices.ASSASSIN]:
        fusion_inventory ="Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name = first_character.name + ' ' + second_character.name,
        class_name=CharactersChoices.FUSION,
        level=(first_character.level + second_character.level)//2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) *1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory= fusion_inventory,

    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    """
    UPDATE character
    SET dexterity = 30
    """
    Character.objects.update(dexterity = 30)


def grand_intelligence():
    Character.objects.update(intelligence = 40)
def grand_strength():
    Character.objects.update(strength = 50)

def delete_characters():
    Character.objects.update(inventory = "The inventory is empty")

