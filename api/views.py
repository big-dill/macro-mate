from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from macro_mate.forms import UserForm, UserProfileForm, MealForm

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from macro_mate.forms import UserForm, UserProfileForm, MealForm

# View for view classes
from django.views import View
# Decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Import taggit models to get all tags
from taggit.models import Tag
# JSON Response for API calls
from django.http import JsonResponse


# Tags API
# --------
# Used for AJAX calls that populate the suggestion box when using tags

class TagsAPI(View):
    @method_decorator(login_required)
    def get(self, request):
        query_set = request.GET

        max_results = query_set.get('max_results', 0)
        search_string = query_set.get('search_string', None)
        try:
            results = self.get_tag_list(max_results=int(max_results),
                                        starts_with=search_string)
        except ValueError:
            return HttpResponse(-1)

        tag_list = [tag.name for tag in results]
       # safe=False because not a dictionary
        return JsonResponse(tag_list, safe=False)

    # Helper function inside class
    def get_tag_list(self, max_results=0, starts_with=''):
        """Returns a list of tags stored in the Tag database model"""
        tag_list = []
        if starts_with:
            tag_list = Tag.objects.filter(name__istartswith=starts_with)
        else:
            tag_list = Tag.objects.all()
        if max_results > 0:
            if len(tag_list) > max_results:
                tag_list = tag_list[:max_results]
        # Ensure a list response from query set for JSON
        return list(tag_list)
