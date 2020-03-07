# Todo
# But a vscode task is setup to do run this
# cmd-shift-p > Tasks:Run Task > populate-db

import random
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'macro_mate_project.settings')

django.setup()

from macro_mate.models import Meal

def add_meal(name, url):
     # randomly assign a list
    m = Meal.objects.get_or_create(name=name, url=url)[0]
    m.categories = get_random_meal_categories()
    
    m.save()


def get_random_meal_categories():
    categories = Meal.MEAL_CATEGORIES
    length = len(categories)
    sampleLength = random.randint(1, length)
    selection = random.sample(Meal.MEAL_CATEGORIES, sampleLength)
    # create comma separated list from first value to store in db
    # as MultiSelectField stores a comma separated char
    return ','.join(str(s[0]) for s in selection)


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

    for meal in meals:
        # add meal to database
        m = add_meal(meal['name'], meal['url'])
        # add random compulsory tag to meal

        # add random optional tag to meal

        # add ingredients to meal


if __name__ == '__main__':
    print('Starting Rango population script')
    populate()
