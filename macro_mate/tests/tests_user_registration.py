import re
import tempfile
from macro_mate import forms
from django.db import models
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from macro_mate.models import UserProfile


class tests_user_registration(TestCase):


    def test_bad_user_registration(self):
        """ checks if when info is left black the post request doesn't go through """
        response = self.client.post('/accounts/register/', {'username': '','email': '', 'password1': '', 'password2': ''})
        self.assertTrue(response.status_code != 302)


    def test_good_user_registration_view(self):
        """ checks post request when info entered in registration view """
        response = self.client.post('/accounts/register/', {'username': 'testuser', 'email': 'test@test.com','password1': 'testabc123','password2': 'testabc123'})
        self.assertEqual(response.status_code, 302)

    def tests_bad_user_login_view(self):
        """ checks post request when info is left blank when attemting to login """
        response = self.client.post('/accounts/login/', {'username': '', 'email': '','password': ''})
        self.assertTrue(response.status_code != 302)

    
    
    def test_good_form_creation(self):
        """ Tests the functionality of the user registration forms.
        Creates a UserProfileForm and UserForm, and attempts to save them.
        tests login with the details if created properly also tests the login view """
        user_data = {'username': 'testuser', 'email': 'test@test.com', 'password': 'testabc123'}

        user = User.objects.get_or_create(username='testuser',
                                            email='test@test.com')[0]
        user.set_password('testabc123')
        user.save()

        response = self.client.post('/accounts/login/', user_data)
        
        self.assertTrue(response.status_code == 302)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(UserProfile.objects.all()), 1)
        self.assertTrue(self.client.login(username='testuser', password='testabc123'))