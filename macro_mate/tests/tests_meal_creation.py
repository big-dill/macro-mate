from macro_mate import forms, models
from populate_macro_mate import populate
from django.db import models
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from macro_mate.models import Meal, MealCategory

def createUser():
    # helper function to register a new user
    user = User.objects.get_or_create(username='testuser',
                                        email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

class tests_meal_creation(TestCase):


    def test_add_meal_creation(self):
        populate()
        numMeals = len(Meal.objects.all())
    # Tests the functionality of the add meal form
        user = createUser()
        self.client.login(username='testuser', password='testabc123')

        meal_data = {
                    'name': 'testmeal',
                    'url': 'http://www.testmeal.com',
                    'servings': '2',
                    'ingredients':'200g Chicken', 
                    'notes':'test notes',
                    'categories':[('1')],
                    'calories_unit':'kcal',
                    'calories_quantity':'100',
                    'fat_unit':'g',
                    'fat_quantity':'10',
                    'protein_unit':'g',
                    'protein_quantity':'10',
                    'carbs_unit':'g',
                    'carbs_quantity':'10',
                    }
        meal_form = forms.MealForm(data=meal_data)
        print(meal_form.errors.as_data())

        self.assertTrue(meal_form.is_valid())
        meal_object = meal_form.save(commit=False)
        meal_object.owner = user.userprofile
        meal_object.save()
        self.assertEqual(len(Meal.objects.all()), numMeals + 1)





    def test_null_add_meal_creation(self):
        populate()
        numMeals = len(Meal.objects.all())
    # tries to add meals when all the values in the form are left blank
        user = createUser()
        self.client.login(username='testuser', password='testabc123')

        meal_data = {
                    'name': '',
                    'url': '',
                    'servings': '',
                    'ingredients':'', 
                    'notes':'',
                    'categories':[('')],
                    'calories_unit':'',
                    'calories_quantity':'',
                    'fat_unit':'',
                    'fat_quantity':'',
                    'protein_unit':'',
                    'protein_quantity':'',
                    'carbs_unit':'',
                    'carbs_quantity':'',
                    }
        meal_form = forms.MealForm(data=meal_data)
        self.assertFalse(meal_form.is_valid())