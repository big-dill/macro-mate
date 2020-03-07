# Todo
# But a vscode task is setup to do run this
# cmd-shift-p > Tasks:Run Task > populate-db

from macro_mate.models import Meal, Ingredient, Meal_Tag, Macro
import random
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'macro_mate_project.settings')

django.setup()


# A dictionary for assigning a demo unit to a Macro label
MACRO_QUANTITY_DICT = {
    Macro.CALORIES: 'kcal',
    Macro.PROTEIN: 'g',
    Macro.FAT: 'g',
    Macro.CARBS: 'g',
}


def add_meal(name, url):
    m = Meal.objects.get_or_create(name=name, url=url)


def populate():
    # Create dictionaries of fake pages
    meals = [
        {'name': 'Spaghetti and Meatballs',
            'url': None},
        {'name': 'Chicken Surprise',
            'url': 'http://www.reciperoulette.tv/#4974'},
        {'name': 'Classic Yorkshire Puddings',
            'url': 'http://www.reciperoulette.tv/#44613'},
        {'name': 'Prawns and aubergine in hoisin sauce',
            'url': 'http://www.reciperoulette.tv/#7883'},
        {'name': 'Italian Bread Soup',
            'url': None}
    ]

    optional_meal_tags = ["vegan", "keto", "meaty", "chunky", "thick"]
    optional_meal_tag_objects = map(add_meal_tag, )

    for meal in meals:
        # add meal to database
        m = add_meal(meal['name'], meal['url'])
        # add random compulsory tag to meal
        add_meal_tag(m)
        # add random optional tag to meal

        # add ingredients to meal

    ingredients = [

    ]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}}

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    for o in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=None):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views if views else random.randint(1, 300)
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


if __name__ == '__main__':
    print('Starting Rango population script')
    populate()
