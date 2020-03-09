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


# Tags API
# --------
# Used for AJAX calls that populate the suggestion box when using tags

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
        return [tag.name for tag in results]
