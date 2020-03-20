# Script to be run on setting up server to correctly provide options for users
# Note: This is NOT a demo populate script, this is for production.

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'macro_mate_project.settings')

django.setup()

from macro_mate.models import MealCategory

# Initialise MealCategories
for cat in MealCategory.MEAL_CATEGORIES:
    c = MealCategory.objects.get_or_create(category=cat)[0]
    c.save()