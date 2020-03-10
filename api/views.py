# Decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# JSON Response for API calls
from django.http import HttpResponse
from django.http import JsonResponse

# View for view classes
from django.views import View

# Import taggit models to get all tags
from taggit.models import Tag

from macro_mate_project.settings import NUTRITION_API_ID, NUTRITION_API_KEY

# Requests for external API call
import json
import requests


# Tags API
# --------
# Used for AJAX calls that populate the suggestion box when using tags
# Some of the query methods are redundant after changing javascript library,
# but left them in...

# API queries:
# max_results -> the maximum number of results to return
# contains -> a search string which searches for tags containing it
# API returns:
# a json list
class TagsAPI(View):
    """ An API for viewing the tags contained in the macro_mate app"""
    @method_decorator(login_required)
    def get(self, request):
        query_set = request.GET

        max_results = query_set.get('max_results', 0)
        contains = query_set.get('contains', None)

        try:
            tag_list = self.get_tag_list(max_results=int(max_results),
                                         contains=contains)
        except ValueError:
            return HttpResponse(-1)

        # safe=False because not a dictionary
        return JsonResponse(tag_list, safe=False)

    def get_tag_list(self, max_results: int = 0, contains: str = ''):
        """Returns a list of tags stored in the Tag database model"""
        if contains:
            results = Tag.objects.filter(name__icontains=contains)
        else:
            results = Tag.objects.all()
        # if max_results is defined
        if max_results > 0:
            # trim list
            if len(results) > max_results:
                results = results[:max_results]
        # Return a list of tag names for json
        return [{'name': tag.name} for tag in results]


# Nutrition API
# --------
# Used for AJAX calls that analyse an ingredient list.
#
# API query:
# title -> recipe title
# ingredients[] -> an array of string ingredients
# servings -> servings

# API returns:
# a heavily chopped up json response from
# https://developer.edamam.com/edamam-docs-nutrition-api


class NutritionAPI(View):
    """ Calls the Edamam API on the server, to prevent API key being exposed """

    TOTAL_NUTRIENTS_FIELD = 'totalNutrients'

    LABEL_LABEL = 'label'
    SERVINGS_LABEL = 'yield'
    CALORIES_LABEL = 'ENERC_KCAL'
    FAT_LABEL = 'FAT'
    CARBS_LABEL = 'CHOCDF'
    PROTEIN_LABEL = 'PROCNT'

    @method_decorator(login_required)
    def get(self, request):
        query_set = request.GET
        # Extract values
        title = query_set.get('title', '')
        ingr = query_set.getlist('ingredients[]')
        servings = query_set.get('servings', '1')

        endpoint = 'https://api.edamam.com/api/nutrition-details'
        payload = {
            'app_id': NUTRITION_API_ID,
            'app_key': NUTRITION_API_KEY
        }
        data = {
            'title': title,
            'ingr': ingr,
            'yield': servings
        }

        r = requests.post(endpoint, params=payload, json=data)

        # Parse the response for our own app
        response_dict = r.json()

        nutrients = response_dict[self.TOTAL_NUTRIENTS_FIELD]

        parsed_response = {
            'servings': response_dict[self.SERVINGS_LABEL],
            'calories': nutrients[self.CALORIES_LABEL],
            'fat': nutrients[self.FAT_LABEL],
            'carbs': nutrients[self.CARBS_LABEL],
            'protein': nutrients[self.PROTEIN_LABEL],
        }

        # delete superfulous labels in response
        for field in parsed_response:
            if isinstance(field, dict):
                field.pop(self.LABEL_LABEL, None)

        print(parsed_response)

        return HttpResponse(json.dumps(parsed_response), content_type="application/json")
