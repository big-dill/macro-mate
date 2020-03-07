# Todo
# But a vscode task is setup to do run this
# cmd-shift-p > Tasks:Run Task > populate-db

import lorem
import random
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'macro_mate_project.settings')

django.setup()

from django.contrib.auth.models import User
from macro_mate.models import Meal

MAX_MEAL_SERVING = 5
MAX_NUTRIENT_QUANTITY = 4000


def add_meal(owner, name, url, tags, ingredients):
    # randomly assign a list
    m = Meal.objects.get_or_create(owner=owner, name=name, url=url)[0]
    # randomly add categories
    m.categories = get_random_meal_categories()
    # randomly add tags (change list to individual args with *)
    m.tags.add(*tags)
    # add random serving
    m.servings = random.randint(0, MAX_MEAL_SERVING)
    # join tags into new line separated list
    m.ingredients = get_char_joined_string(ingredients, "\n")
    # Randomly generate some lorum for the notes
    m.notes = lorem.paragraph() if random.choice([True, False]) else ''
    # Add nutrients (default units will be used)
    m.calorie_quantity = random.uniform(0, MAX_NUTRIENT_QUANTITY)
    m.fat_quantity = random.uniform(0, MAX_NUTRIENT_QUANTITY)
    m.protein_quantity = random.uniform(0, MAX_NUTRIENT_QUANTITY)
    m.carbs_quantity = random.uniform(0, MAX_NUTRIENT_QUANTITY)

    m.save()

    return m


def get_char_joined_string(collection, char):
    return str(char).join(str(item) for item in collection)


def get_random_meal_categories():
    selection = get_random_sample(Meal.MEAL_CATEGORIES)
    # get first value from tuples in MEAL_CATEGORIES for db population
    selection = [s[0] for s in selection]
    # create comma separated list from first value to store in db
    # as MultiSelectField stores a comma separated char
    return get_char_joined_string(selection, ',')


def get_random_sample(collection):
    length = len(collection)
    sampleLength = random.randint(1, length)
    selection = random.sample(collection, sampleLength)
    return selection


def add_user(username):
    user = User.objects.create_user(
        username=username,
        email=username + "@gmail.com",
        password=username
    )
    user.save()
    return user


def populate():
    # Create dictionaries of fake pages
    meal_names = [
        'Spaghetti and Meatballs',
        'Chicken Surprise',
        'Classic Yorkshire Puddings',
        'Prawns and Aubergine in Hoisin Sauce',
        'Italian Bread Soup'
    ]

    meal_urls = [
        '',
        'http://www.reciperoulette.tv/#4974',
        'http://www.reciperoulette.tv/#44613'
    ]

    meal_tags = [
        "keto",
        "vegetarian",
        "chunky",
        "gluten-free",
        "high-protein",
    ]

    meal_ingredients = [
        '20oz Raw Brocolli',
        '200g Chicken',
        '70g Sweetcorn',
        '100g Turkey',
        '20g Broccoli'
    ]

    users = [
        'julia',
        'hugh',
        'mark'
    ]

    # Delete all existing users that aren't superusers
    User.objects.filter(is_superuser=False).delete()

    for name in users:
        user = add_user(name)
        print("here")
        # Add a random amount of meals between 1 and 10
        for i in range(random.randint(1, 10)):
            add_meal(user.user_profile,
                     random.choice(meal_names),
                     random.choice(meal_urls),
                     get_random_sample(meal_tags),
                     get_random_sample(meal_ingredients))


if __name__ == '__main__':
    print('Starting Rango population script')
    populate()
