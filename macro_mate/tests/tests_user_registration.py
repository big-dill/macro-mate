import os
import re
import inspect
import tempfile
from macro_mate import forms, models
from django.db import models
from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields


class tests_user_registration(TestCase):


    def test_bad_user_registration(self):
    # checks if when info is left black the post request doesn't go through
        response = self.client.post('/accounts/register/', {'username': '','email': '', 'password1': '', 'password2': ''})
        self.assertTrue(response.status_code != 302)


    def test_good_user_registration_view(self):
    # checks post request when info entered in registration view
        response = self.client.post('/accounts/register/', {'username': 'testuser', 'email': 'test@test.com','password1': 'testabc123','password2': 'testabc123'})
        self.assertEqual(response.status_code, 302)

    def tests_bad_user_login_view(self):
    # checks post request when info is left blank when attemting to login
        response = self.client.post('/accounts/login/', {'username': '', 'email': '','password': ''})
        self.assertTrue(response.status_code != 302)

    
    
    def test_good_form_creation(self):
    # Tests the functionality of the user registration forms.
    # Creates a UserProfileForm and UserForm, and attempts to save them.
    # tests login with the details if created properly also tests the login view

        user_data = {'username': 'testuser123', 'email': 'test@test.com', 'password': 'test123'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid())
        self.assertTrue(user_profile_form.is_valid())

        user_object = user_form.save()
        user_object.set_password(user_object.password)
        user_object.save()
        
        profile_object = user_profile_form.save(commit=False)
        profile_object.user = user_object
        profile_object.save()

        response = self.client.post('/accounts/login/', user_data)
        
        self.assertTrue(response.status_code == 302)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(macro_mate.models.UserProfile.objects.all()), 1)
        self.assertTrue(self.client.login(username='testuser123', password='test123'))