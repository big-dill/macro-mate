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
from macro_mate.models import Meal, MealCategory, Comment

MIN_MEAL_SERVING = 1
MAX_MEAL_SERVING = 5
MIN_NUTRIENT_QUANTITY = 1
MAX_NUTRIENT_QUANTITY = 4000


def add_meal(owner, userprofiles, name, url, tags, ingredients):
    # randomly assign a list
    m = Meal.objects.get_or_create(owner=owner, name=name, url=url)[0]

    # randomly add tags (change list to individual args with *)
    m.tags.add(*tags)
    # add random serving
    m.servings = random.randint(MIN_MEAL_SERVING, MAX_MEAL_SERVING)
    # join tags into new line separated list
    m.ingredients = get_char_joined_string(ingredients, "\n")
    # Randomly generate some lorum for the notes
    m.notes = lorem.paragraph() if random.choice([True, False]) else ''
    # Add nutrients (default units will be used)
    m.calories_quantity = random.uniform(
        MIN_NUTRIENT_QUANTITY, MAX_NUTRIENT_QUANTITY)
    m.fat_quantity = random.uniform(
        MIN_NUTRIENT_QUANTITY, MAX_NUTRIENT_QUANTITY)
    m.protein_quantity = random.uniform(
        MIN_NUTRIENT_QUANTITY, MAX_NUTRIENT_QUANTITY)
    m.carbs_quantity = random.uniform(
        MIN_NUTRIENT_QUANTITY, MAX_NUTRIENT_QUANTITY)

    # Add random comments from users who have that meal in their accounts...
    commenting_userprofiles = get_random_sample(userprofiles)
    for userprofile in commenting_userprofiles:
        Comment.objects.get_or_create(
            owner=userprofile,
            meal=m,
            body=lorem.paragraph()
        )

    m.save()

    # randomly add categories after save (as many to many field)
    m.categories.set(get_random_meal_categories())
    # randomly add users who reference this meal
    m.users.set(userprofiles)

    return m


def get_char_joined_string(collection, char):
    return str(char).join(str(item) for item in collection)


def get_random_meal_categories():
    selection = get_random_sample(list(MealCategory.objects.all()))
    print(selection)
    return selection


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
        'tim',
        'jane',
        'sebastian',
        'elizabeth'
    ]

    # Delete all existing users that aren't superusers
    User.objects.filter(is_superuser=False).delete()

    # Initialise MealCategories
    for cat in MealCategory.MEAL_CATEGORIES:
        c = MealCategory.objects.get_or_create(category=cat)[0]
        c.save()

    # Initialise Mock Users
    for name in users:
        user = add_user(name)

    # Get the users from the newly created user list
    users = User.objects.all()
    # Get the profiles of each user for meal association
    userprofiles = [user.userprofile for user in users]

    for user in users:
        # Add a random amount of meals between 1 and 10 that they own
        for i in range(random.randint(1, 10)):
            userprofile = user.userprofile
            # Add random users who have the meal in their account,
            random_userprofiles = set(get_random_sample(userprofiles))
            #  including the creator
            random_userprofiles.add(userprofile)

            print(random_userprofiles)

            add_meal(
                # Set user as the owner
                userprofile,
                # Add the meal to a random selection of user's accounts
                random_userprofiles,
                # Name their version of the meal
                random.choice(meal_names),
                # Randomly assign a URL
                random.choice(meal_urls),
                # Randomly assign meal_tags
                get_random_sample(meal_tags),
                # Randomly assign ingredients
                get_random_sample(meal_ingredients)
            )


if __name__ == '__main__':
    print('Starting Rango population script')
    populate()
