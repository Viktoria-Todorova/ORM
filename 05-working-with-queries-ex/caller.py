import os
from typing import List

import django
from django.db.models import Case, When, Value

from main_app.choices import OperationSystemChoices, MealTypeChoices, DificultyChoices, WorkoutTypeChoices

# from populate_db import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout


#from typing import List

# Create and check models
# Run and print your queries

#1 Artwork Gallery

def show_highest_rated_art() -> str:
    highest_rating = ArtworkGallery.objects.order_by('-rating','id').first()
    return f"{highest_rating.art_name} is the highest-rated art with a {highest_rating.rating} rating!"

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()

# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
#
# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())


#2
def show_the_most_expensive_laptop()->str:
    expensive = Laptop.objects.order_by('-price','-id').first()
    return f"{expensive.brand} is the most expensive laptop available for {expensive.price}$!"

def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage()->None:
    Laptop.objects.filter(brand__in=['Asus','Lenovo']).update(storage=512)

def update_to_16_GB_memory()->None:
    Laptop.objects.filter(brand__in=['Apple','Dell','Acer']).update(memory=16)

def update_operation_systems()->None:
    Laptop.objects.update(
        operation_system = Case(
            When(brand='Asus',then=Value(OperationSystemChoices.WINDOWS)),
            When(brand='Apple', then=Value(OperationSystemChoices.MACOS)),
            When(brand='Lenovo', then=Value(OperationSystemChoices.CHROMEOS)),
            When(brand__in=['Acer','Dell'], then=Value(OperationSystemChoices.LINUX))

        )
    )
    # Laptop.objects.filter(brand='Asus').update(operating_system=OperationSystemChoices.WINDOWS)
    # Laptop.objects.filter(brand='Apple').update(operating_system=OperationSystemChoices.MACOS)
    # Laptop.objects.filter(brand='Lenovo').update(operating_system=OperationSystemChoices.CHROMEOS)
    # Laptop.objects.filter(brand__in=['Acer','Dell']).update(operating_system=OperationSystemChoices.LINUX)

def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_GB_storage()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)



#3



def bulk_create_chess_players(args: List[ChessPlayer])->None:
    ChessPlayer.objects.bulk_create(args)

def delete_chess_players()->None:
    ChessPlayer.objects.filter(title ='no title').delete()

def change_chess_games_won()->None:
    ChessPlayer.objects.filter(title='GM').update(games_won=30)

def change_chess_games_lost()->None:
    ChessPlayer.objects.filter(title ='no title').update(games_lost=25)

def change_chess_games_drawn()->None:
    ChessPlayer.objects.update(games_drawn=10)

def grand_chess_title_GM()->None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')

def grand_chess_title_IM()->None:
    ChessPlayer.objects.filter(rating__range=[2300,2399]).update(title='IM')

def grand_chess_title_FM()->None:
    ChessPlayer.objects.filter(rating__range=[2200,2299]).update(title='FM')

def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title='regular player')


#4
# •	If the meal type is "Breakfast", update the chef's name to "Gordon Ramsay".
# •	If the meal type is "Lunch", update the chef's name to "Julia Child".
# •	If the meal type is "Dinner", update the chef's name to "Jamie Oliver".
# •	If the meal type is "Snack", update the chef's name to "Thomas Keller".

def set_new_chefs():
    Meal.objects.filter(meal_type=MealTypeChoices.BREAKFAST).update(chef='Gordon Ramsay')
    Meal.objects.filter(meal_type=MealTypeChoices.LUNCH).update(chef='Julia Child')
    Meal.objects.filter(meal_type=MealTypeChoices.DINNER).update(chef='Jamie Oliver')
    Meal.objects.filter(meal_type=MealTypeChoices.SNACK).update(chef='Thomas Keller')


# •	If the meal type is "Breakfast", update the preparation time to "10 minutes".
# •	If the meal type is "Lunch", update the preparation time to "12 minutes".
# •	If the meal type is "Dinner", update the preparation time to "15 minutes".
# •	If the meal type is "Snack", update the preparation time to "5 minutes".

def set_new_preparation_times()->None:
    Meal.objects.filter(meal_type=MealTypeChoices.BREAKFAST).update(preparation_time=10)
    Meal.objects.filter(meal_type=MealTypeChoices.LUNCH).update(preparation_time=12)
    Meal.objects.filter(meal_type=MealTypeChoices.DINNER).update(preparation_time=15)
    Meal.objects.filter(meal_type=MealTypeChoices.SNACK).update(preparation_time=5)

def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoices.BREAKFAST,MealTypeChoices.DINNER]).update(calories=400)

def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH,MealTypeChoices.SNACK]).update(calories=700)

def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH,MealTypeChoices.SNACK]).delete()



#5


def show_hard_dungeons()->str:
    hard_choices = Dungeon.objects.filter(difficulty=DificultyChoices.HARD).order_by('-location')
    return '\n'.join(f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!" for d in hard_choices)

def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)

# •	If the dungeon difficulty is "Easy", update the dungeon name to "The Erased Thombs".
# •	If the dungeon difficulty is "Medium", update the dungeon name to "The Coral Labyrinth".
# •	If the dungeon difficulty is "Hard", update the dungeon name to "The Lost Haunt".

def update_dungeon_names():
    Dungeon.objects.filter(difficulty=DificultyChoices.EASY).update(name="The Erased Thombs")
    Dungeon.objects.filter(difficulty=DificultyChoices.MEDIUM).update(name="The Coral Labyrinth")
    Dungeon.objects.filter(difficulty=DificultyChoices.HARD).update(name="The Lost Haunt")

#() changes the boss health to 500 for all dungeons except for the ones that have difficulty "Easy".
def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty=DificultyChoices.EASY).update(boss_health=500)

# •	If the dungeon difficulty is "Easy", update the recommended level to 25.
# •	If the dungeon difficulty is "Medium", update the recommended level to 50.
# •	If the dungeon difficulty is "Hard", update the recommended level to 75.

def update_dungeon_recommended_levels():
    # Dungeon.objects.filter(difficulty=DificultyChoices.EASY).update(recommended_level=25)
    # Dungeon.objects.filter(difficulty=DificultyChoices.MEDIUM).update(recommended_level=50)
    # Dungeon.objects.filter(difficulty=DificultyChoices.HARD).update(recommended_level=75)
    Dungeon.objects.update(recommended_level =Case(
        When(difficulty=DificultyChoices.EASY,then=Value(25)),
        When(difficulty=DificultyChoices.MEDIUM, then=Value(50)),
        When(difficulty=DificultyChoices.HARD, then=Value(75)),
    ))

# •	If the dungeon boss's health is 500, update the dungeon reward to "1000 Gold".
# •	If the dungeon's location starts with "E", update the reward to "New dungeon unlocked".
# •	If the dungeon's location ends with "s", update the reward to "Dragonheart Amulet".

def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health=500).update(reward=1000)
    Dungeon.objects.filter(location__startswith='E').update(reward="New dungeon unlocked")
    Dungeon.objects.filter(location__endswith='s').update(reward="Dragonheart Amulet")


# •	If the recommended level is 25, update the dungeon location to "Enchanted Maze".
# •	If the recommended level is 50, update the dungeon location to "Grimstone Mines".
# •	If the recommended level is 75, update the dungeon location to "Shadowed Abyss".

def set_new_locations():
    # Dungeon.objects.filter(recommended_level=25).update(location="Enchanted Maze")
    # Dungeon.objects.filter(recommended_level=50).update(location="Grimstone Mines")
    # Dungeon.objects.filter(recommended_level=75).update(location="Shadowed Abyss")

    Dungeon.objects.update(location= Case(
        When(recommended_level=25,then=Value("Enchanted Maze")),
        When(recommended_level=50, then=Value("Grimstone Mines")),
        When(recommended_level=75, then=Value("Shadowed Abyss")),
    ))



#6

#•	"{workout_name_1} from {workout_type_1} type has {difficulty_1} difficulty!
def show_workouts():
    workouts =Workout.objects.filter(workout_type__in = [WorkoutTypeChoices.CALISTHENICS,WorkoutTypeChoices.CROSSFIT,]).order_by('id')
    return '\n'.join(f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!" for w in workouts)

#returns all workouts from type "Cardio" that have difficulty "High", ordered by the instructor.
def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(workout_type=WorkoutTypeChoices.CARDIO,
                                  dificulty= "Hard").order_by('instructor')

# •	If the workout type is "Cardio", update the instructor to "John Smith".
# •	If the workout type is "Strength", update the instructor to "Michael Williams".
# •	If the workout type is "Yoga", update the instructor to "Emily Johnson".
# •	If the workout type is "CrossFit", update the instructor to "Sarah Davis".
# •	If the workout type is "Calisthenics", update the instructor to "Chris Heria".

def set_new_instructors():
    Workout.objects.update(instructor=Case(
        When(workout_type=WorkoutTypeChoices.CARDIO,then=Value("John Smith")),
        When(workout_type=WorkoutTypeChoices.STRENGTH, then=Value("Michael Williams")),
        When(workout_type=WorkoutTypeChoices.YOGA, then=Value("Emily Johnson")),
        When(workout_type=WorkoutTypeChoices.CROSSFIT, then=Value("Sarah Davis")),
        When(workout_type=WorkoutTypeChoices.CALISTHENICS, then=Value("Chris Heria")),

    ))
# •	If the instructor is "John Smith", update the duration time to "15 minutes".
# •	If the instructor is "Sarah Davis", update the duration time to "30 minutes".
# •	If the instructor is "Chris Heria", update the duration time to "45 minutes".
# •	If the instructor is "Michael Williams", update the duration time to "1 hour".
# •	If the instructor is "Emily Johnson", update the duration time to "1 hour and 30 minutes".

def set_new_duration_times():
    Workout.objects.update(duration_time=Case(
        When(instructor="John Smith", then=Value("15 minutes")),
        When(instructor="Sarah Davis", then=Value("30 minutes")),
        When(instructor="Chris Heria", then=Value("45 minutes")),
        When(instructor="Michael Williams", then=Value("1 hour")),
        When(instructor="Emily Johnson", then=Value("1 hour and 30 minutes")),
    ))

def delete_workouts():
    Workout.objects.exclude(workout_type__in=[WorkoutTypeChoices.STRENGTH,WorkoutTypeChoices.CALISTHENICS]).delete()


