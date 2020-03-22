from macro_mate import forms
from populate_macro_mate import populate
from django.db import models
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from macro_mate.models import Meal

def createUser():
    # helper function to register a new user
    user = User.objects.get_or_create(username='testuser',
                                        email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

class tests_meal_creation(TestCase):
    meal_data = {
            'name': 'testmeal',
            'url': 'http://www.testmeal.com',
            'servings': '2',
            'ingredients':'200g Chicken, 20g tomatoes',
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
    meal_data_null = {
            'name':'',
            'url':'',
            'servings':'',
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

    def test_good_meal_view(self):
        """ A test for checking the add meal view when submitting valid data """
        populate()
        user = createUser()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.post('/macro_mate/add_meal/', data=tests_meal_creation.meal_data)
        self.assertEqual(response.status_code, 302)

    def test_bad_meal_view(self):
        """ A test for checking the add meal view when submitting invalid data """
        populate()
        user = createUser()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.post('/macro_mate/add_meal/', data=tests_meal_creation.meal_data_null)
        self.assertNotEqual(response.status_code, 302)
    


    def test_add_meal_creation(self):
        """ A test for checking the creation of a meal object with valid data"""
        populate()
        numMeals = len(Meal.objects.all())
    # Tests the functionality of the add meal form
        user = createUser()
        self.client.login(username='testuser', password='testabc123')
        meal_form = forms.MealForm(data=tests_meal_creation.meal_data)
        print(meal_form.errors.as_data())

        self.assertTrue(meal_form.is_valid())
        meal_object = meal_form.save(commit=False)
        meal_object.owner = user.userprofile
        meal_object.save()
        self.assertEqual(len(Meal.objects.all()), numMeals + 1)





    def test_null_add_meal_creation(self):
        """ A test for checking the creation of a meal object with invalid data"""
        populate()
        numMeals = len(Meal.objects.all())
    # tries to add meals when all the values in the form are left blank
        createUser()
        self.client.login(username='testuser', password='testabc123')

        meal_form = forms.MealForm(data=tests_meal_creation.meal_data_null)
        self.assertFalse(meal_form.is_valid())


    def test_update_meal_creation(self):
        """ A test for checking that a meal can be updated """
        populate()
    # tests the update meal function
        user = createUser()
        self.client.login(username='testuser', password='testabc123')
        meal_form = forms.MealForm(data=tests_meal_creation.meal_data)

        print(meal_form.errors.as_data())
        self.assertTrue(meal_form.is_valid())
        meal_object = meal_form.save(commit=False)
        meal_object.owner = user.userprofile
        meal_object.save()
        numMeals = len(Meal.objects.all())
        meal = meal_object
        meal.owner = user.userprofile
        meal_data_updated = {
                    'name': 'testmeal2updated',
                    'url': 'http://www.testmeal.com',
                    'servings': '2',
                    'ingredients':'200g Chicken', 
                    'notes':'test notes',
                    'categories':[('1')],
                    'calories_unit':'kcal',
                    'calories_quantity':'10',
                    'fat_unit':'g',
                    'fat_quantity':'20',
                    'protein_unit':'g',
                    'protein_quantity':'20',
                    'carbs_unit':'g',
                    'carbs_quantity':'20',
                    }
        meal_form = forms.MealForm(data=meal_data_updated, instance=meal)
        print(meal_form.errors.as_data())
        self.assertTrue(meal_form.is_valid())
        meal_object = meal_form.save(commit=False)
        meal_object.owner = user.userprofile
        meal_object.save()
        # makes sure meal is updated and not just a new instance created
        self.assertTrue(meal.name == 'testmeal2updated')
        self.assertTrue(meal_object.name == 'testmeal2updated')
        self.assertEqual(numMeals,len(Meal.objects.all()) )
        