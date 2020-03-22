import os
from django.test import TestCase
from django.conf import settings
from django.urls import reverse

class tests_urls_templates(TestCase):

    def test_url_usage(self):
        # tests that all the urls used are associated with the right html
        urls = [reverse('macro_mate:index'),
                reverse('macro_mate:meal'),
                reverse('macro_mate:meals'),
                reverse('macro_mate:my_meals'),]

        templates = ['macro_mate/index.html',
                    'macro_mate/meal.html',
                    'macro_mate/all_meals.html',
                    'macro_mate/meal_list.html',]
            
        for url, template in zip(urls, templates):
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)

    def test_base_template_exists(self):
        # ensures theres a base template that is being inherited from
            template_base_path = os.path.join(settings.TEMPLATE_DIR, 'macro_mate', 'base.html')
            self.assertTrue(os.path.exists(template_base_path))
