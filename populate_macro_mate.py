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

from macro_mate.models import Meal


def add_meal(name, url, tags):
    # randomly assign a list
    m = Meal.objects.get_or_create(name=name, url=url)[0]
    # randomly add categories
    m.categories = get_random_meal_categories()
    # randomly add tags (change list to individual args with *)
    m.tags.add(*tags)
    # Randomly generate some lorum for the notes
    m.notes = lorem.paragraph() if random.choice([True, False]) else ''
    m.save()


def get_random_meal_categories():
    selection = get_random_sample(Meal.MEAL_CATEGORIES)
    # create comma separated list from first value to store in db
    # as MultiSelectField stores a comma separated char
    return ','.join(str(s[0]) for s in selection)


def get_random_sample(collection):
    length = len(collection)
    sampleLength = random.randint(1, length)
    selection = random.sample(collection, sampleLength)
    return selection


def populate():
    # Create dictionaries of fake pages
    meals = [
        {'name': 'Spaghetti and Meatballs',
            'url': ''},
        {'name': 'Chicken Surprise',
            'url': 'http://www.reciperoulette.tv/#4974'},
        {'name': 'Classic Yorkshire Puddings',
            'url': 'http://www.reciperoulette.tv/#44613'},
        {'name': 'Prawns and aubergine in hoisin sauce',
            'url': 'http://www.reciperoulette.tv/#7883'},
        {'name': 'Italian Bread Soup',
            'url': ''}
    ]

    tags = [
        "keto",
        "vegetarian",
        "chunky",
        "gluten-free",
        "high-protein",
    ]

    for meal in meals:
        # add meal to database
        m = add_meal(meal['name'], meal['url'], get_random_sample(tags))
        # add random compulsory tag to meal

        # add random optional tag to meal

        # add ingredients to meal


if __name__ == '__main__':
    print('Starting Rango population script')
    populate()
