import os
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from populate_macro_mate import populate


def createUser():
    user = User.objects.get_or_create(username='testuser',
                                        email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

class tests_urls_templates(TestCase):

    def test_url_usage(self):
        """ A test for checking the correct page is loaded with each url"""
        populate()
        user = createUser()
        self.client.login(username='testuser', password='testabc123')
        # tests that all the urls used are associated with the right html
        urls = ['/macro_mate/',
                '/macro_mate/meal/12/',
                '/macro_mate/meals/',
                '/macro_mate/my_meals/',
                '/macro_mate/add_meal/',]

        templates = ['macro_mate/index.html',
                    'macro_mate/meal.html',
                    'macro_mate/all_meals.html',
                    'macro_mate/all_meals.html',
                    'macro_mate/add_meal.html',]
            
        for url, template in zip(urls, templates):
            response = self.client.get(url, follow=True)
            self.assertTemplateUsed(response, template)
