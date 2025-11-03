""""
1.pip install sqlalchemy
2. pip install alembic
3.pip install psycopg2-binary
4.create db
5.create file for models
6.Create Base class
7.alembic init alembic
8. Tell alembic which is our base model target_metadata = Base.metadata
9.Tell alembic how to connect to the db sqlalchemy.url = postgresql+psycopg2://postgres:200697@localhost/sql_alchemy_ex
10. After creating the model : alembic revision --autogenerate -m "Created Recipe Model"
11. make migration :  alembic upgrade head
12.     engine = create_engine('postgresql+psycopg2://postgres:200697@localhost/sql_alchemy_ex')
        Session = sessionmaker(engine=engine)
        session = Session()
"""
import os
from typing import List, Type

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers import handle_session
from models import Recipe, Chef

load_dotenv()
engine = create_engine(f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@localhost/sql_alchemy_ex')
Session = sessionmaker(bind=engine)
session = Session()

# session.begin()
# session.commit()
# session.close()

#1

@handle_session(session)
def create_recipe(name: str, ingredients: str, instructions: str):
    new_recipe = Recipe(name=name, ingredients=ingredients,instructions=instructions)

    session.add(new_recipe)

# create_recipe(
# "Spaghetti Carbonara	Pasta",
#     "Eggs, Pancetta, Cheese",
#     "Cook the pasta, mix it with eggs, pancetta, and cheese"
# )

# # Query all recipes
#  = session.query(Recipe).all()
#
# # Loop through each recipe and print its details
# for recipe in recipes:
#     print(f"Recipe name: {recipe.name}")

#3
@handle_session(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str) -> None:
    #version 1
    # recipe_to_update = session.query(Recipe).filter(name= name).one()
    # recipe_to_update.name = new_name
    # recipe_to_update.ingredients = new_ingredients
    # recipe_to_update.instructions = new_instructions
    # #we dont save cuz the decorator is doing it

    #version 2
    session.query(Recipe).filter_by(name=name).update({
        Recipe.name: new_name,
        Recipe.ingredients: new_ingredients,
        Recipe.instructions: new_instructions
    })
update_recipe_by_name('Spaghetti Carbonara	Pasta', 'test', 'test', 'test')
#
# # Update a recipe by name
# update_recipe_by_name(
#     name="Spaghetti Carbonara",
#     new_name="Carbonara Pasta",
#     new_ingredients="Pasta, Eggs, Guanciale, Cheese",
#     new_instructions="Cook the pasta, mix with eggs, guanciale, and cheese"
# )
#
# # Query the updated recipe
# updated_recipe = session.query(Recipe).filter_by(name="Carbonara Pasta").first()
#
# # Print the updated recipe details
# print("Updated Recipe Details:")
# print(f"Name: {updated_recipe.name}")
# print(f"Ingredients: {updated_recipe.ingredients}")
# print(f"Instructions: {updated_recipe.instructions}")

#4
@handle_session(session)
def delete_recipe_by_name(name: str):
    session.query(Recipe).filter_by(name=name).delete()

# # Delete a recipe by name
# delete_recipe_by_name("test")
#
# # Query all recipes
# recipes = session.query(Recipe).all()
#
# # Loop through each recipe and print its details
# for recipe in recipes:
#     print(f"Recipe name: {recipe.name}")

#5

@handle_session(session,autoclose=False)
def get_recipes_by_ingredient(ingredient_name: str) -> list[Type[Recipe]]:
    # for harder filterin
    return session.query(Recipe).filter(Recipe.ingredients.ilike(f"%{ingredient_name}%")).all()

# # Delete all objects (recipes) from the database
# session.query(Recipe).delete()
# session.commit()
#
# # Create three Recipe instances with two of them sharing the same ingredient
# recipe1 = create_recipe(
#     'Spaghetti Bolognese',
#     'Ground beef, tomatoes, pasta',
#     'Cook beef, add tomatoes, serve over pasta'
# )
#
# recipe2 = create_recipe(
#     'Chicken Alfredo',
#     'Chicken, fettuccine, Alfredo sauce',
#     'Cook chicken, boil pasta, mix with sauce'
# )
#
# recipe3 = create_recipe(
#     'Chicken Noodle Soup',
#     'Chicken, noodles, carrots',
#     'Boil chicken, add noodles, carrots'
# )
#
# # Run the function and print the results
# ingredient_to_filter = 'Chicken'
# filtered_recipes = get_recipes_by_ingredient('Chicken')
#
# print(f"Recipes containing {ingredient_to_filter}:")
# for recipe in filtered_recipes:
#     print(f"Recipe name - {recipe.name}")
#
# session.close()

#6
@handle_session(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str):
    first_recipe =( session.query(Recipe).
                    filter_by(name=first_recipe_name)
                    .with_for_update()
                    .one())
    second_recipe = (session.query(Recipe)
                     .filter_by(name=second_recipe_name)
                    .with_for_update()  #locks the recors preventing others to modify in untill its migrated
                     .one())

    first_recipe.ingredients,second_recipe.ingredients = second_recipe.ingredients,first_recipe.ingredients

# # Delete all objects (recipes) from the database
# session.query(Recipe).delete()
# session.commit()
#
# # Create the first recipe
# create_recipe("Pancakes", "Flour, Eggs, Milk", "Mix and cook on a griddle")
#
# # Create the second recipe
# create_recipe("Waffles", "Flour, Eggs, Milk, Baking Powder", "Mix and cook in a waffle iron")
#
# # Now, swap their ingredients
# swap_recipe_ingredients_by_name("Pancakes", "Waffles")
#
# recipe1 = session.query(Recipe).filter_by(name="Pancakes").first()
# recipe2 = session.query(Recipe).filter_by(name="Waffles").first()
# print(f"Pancakes ingredients {recipe1.ingredients}")
# print(f"Waffles ingredients {recipe2.ingredients}")

#
#9
@handle_session(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) ->str:
    recipe =session.query(Recipe).filter_by(name=recipe_name).one()

    if recipe.chef:
        raise Exception("Recipe: {recipe_name} already has a related chef")
    chef = session.query(Chef).filter_by(name=chef_name).one()
    recipe.chef = chef
    return f"Related recipe {recipe_name} with chef {chef_name}"

# # Create a recipe instance for Bulgarian Musaka
# musaka_recipe = Recipe(
#     name="Musaka",
#     ingredients="Potatoes, Ground Meat, Onions, Eggs, Milk, Cheese, Spices",
#     instructions="Layer potatoes and meat mixture, pour egg and milk mixture on top, bake until golden brown."
# )
#
# # Create a Bulgarian chef instances
# bulgarian_chef1 = Chef(name="Ivan Zvezdev")
# bulgarian_chef2 = Chef(name="Uti Buchvarov")
#
# # Add the recipe instance to the session
# session.add(musaka_recipe)
#
# # Add the chef instances to the session
# session.add(bulgarian_chef1)
# session.add(bulgarian_chef2)
#
# # Commit the changes to the database
# session.commit()
#
# print(relate_recipe_with_chef_by_name("Musaka","Ivan Zvezdev"))

#10
@handle_session(session)
def get_recipes_with_chef()->str:
    recipies_with_chef = (
        session.query(Recipe.name, Chef.name)
        .join(Chef,Recipe.chef).all()
    )

    return '\n'.join(f"Recipe: {recipe_name} made by chef: {chef_name}" for recipe_name,chef_name in recipies_with_chef)


