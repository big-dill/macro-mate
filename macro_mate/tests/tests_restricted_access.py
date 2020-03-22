from django.db import models
from django.test import TestCase
from django.contrib.auth.models import User

def createUser():
    user = User.objects.get_or_create(username='testuser',
                                        email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

class tests_restricted_access(TestCase):

    def test_bad_add_meal(self):
        """ A test for checking add meal access when not logged in """
        response = self.client.get('/macro_mate/add_meal/')
        self.assertNotEqual(response.status_code, 200)


    def test_good_add_meal(self):
        """ A test for checking add meal access when logged in """
        createUser()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get('/macro_mate/add_meal/')
        self.assertEqual(response.status_code, 200)

    def test_good_my_meal_view(self):
        """ A test for checking my meal access when not logged in """
        createUser()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get('/macro_mate/my_meals/')
        self.assertEqual(response.status_code, 200)

    def test_bad_my_meal_view(self):
        """ A test for checking my meal access when logged in """
        response = self.client.get('/macro_mate/my_meals/')
        self.assertNotEqual(response.status_code, 200)
