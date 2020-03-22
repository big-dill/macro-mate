import os
import re
import inspect
import tempfile
from macro_mate import forms, models, urls
from django.db import models
from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

def createUser():
    user = User.objects.get_or_create(username='testuser',
                                        email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

class tests_restricted_access(TestCase):

    def test_bad_add_meal(self):
        response = self.client.get('/macro_mate/add_meal/')
        self.assertNotEqual(response.status_code, 200)


    def test_good_add_meal(self):
        user = createUser()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get('/macro_mate/add_meal/')
        self.assertEqual(response.status_code, 200)
