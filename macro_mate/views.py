from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from macro_mate.forms import MealForm, CommentForm

from macro_mate.models import Meal, MealCategory
from taggit.models import Tag

# decorator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    TEMPLATE = 'macro_mate/index.html'
    response = render(request, TEMPLATE, context={})
    return response


def meal(request, meal_id_slug):
    """Displays the meal with a comment form"""

    TEMPLATE = "macro_mate/meal.html"

    # 404 if no meal found
    mealget = get_object_or_404(Meal, id=meal_id_slug)
    user = request.user
    is_owner = mealget.owner == user.userprofile
    ingredients = mealget.ingredients.split('\n')
    comments = mealget.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.owner = user.userprofile
            # Assign the current meal to the comment
            new_comment.meal = mealget
            # Save the comment to the database
            new_comment.save()

            # Redirect to the same url, but for 'get'
            return HttpResponseRedirect(request.path)

    else:
        if user.is_authenticated:
            comment_form = CommentForm()
        else:
            comment_form = None

    return render(request, TEMPLATE, context={
        'is_owner': is_owner,
        'meal': mealget,
        'picture': mealget.image,
        'ingredients': ingredients,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


class AllMeals(TemplateView):
    """ A view for viewing all meals """

    template_name = 'macro_mate/all_meals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        meals = Meal.objects.all()

        tag_slug = self.kwargs.get('slug', None)

        if(tag_slug):
            try:
                tag = Tag.objects.get(slug=tag_slug)
                context['tag'] = tag
                meals = meals.filter(tags__name__in=[tag.name])
            except Tag.DoesNotExist:
                # Ignore modifying self.meals if no tags are found
                # Signal in context_dict so an error message can be displayed
                # For error displays
                context['tag_slug'] = tag_slug
                context['tag_error'] = True

        context['recent_meals'] = meals.order_by('-created_date')[0:6]

        categories = [{'name': cat, 'meals': meals.filter(
            categories__category=cat)} for cat in MealCategory.MEAL_CATEGORIES]

        context['categories'] = categories

        # get all tags
        context['tags'] = Tag.objects.all().order_by('name')

        context['meals'] = meals

        return context


class MyMeals(LoginRequiredMixin, AllMeals):
    """ A view for viewing the current logged in user's meals.
    Inherits from AllMeals and uses the LoginRequiredMixin to ensure that the user is logged in """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['meals'] = context['meals'].filter(owner=user.userprofile)
        context['recent_meals'] = context['meals'].order_by(
            '-created_date')[0:6]

        for cat in context['categories']:
            cat['meals'] = cat['meals'].filter(owner=user.userprofile)

        # print([meal.name for meal in context['meals'].all()])
        context['username'] = user.username
        context['user_id'] = user.id
        return context


class AddMeal(View):
    """ A view for adding a meal to the database """

    TEMPLATE = "macro_mate/add_meal.html"

    @method_decorator(login_required)
    def get(self, request, meal_id_slug):
        """ Display the form for adding / editing a meal """

        form = MealForm()
        # If the user is trying to edit a pre-existing meal
        if(meal_id_slug):
            # 404 if no meal found
            mealget = get_object_or_404(Meal, id=meal_id_slug)
            user = request.user

            # Forbidden page if they are not the owner of the meal
            if (mealget.owner != user.userprofile):
                return HttpResponseForbidden()
            else:
                # Otherwise, fill the form in with the meal and return

                # Parse the tag fields to a comma separated list
                parsed_tags = ",".join(
                    [tag.name for tag in mealget.tags.all()])

                form = MealForm(
                    initial={'tags': parsed_tags}, instance=mealget)

        return render(request, self.TEMPLATE, context={
            'form': form
        })

    @method_decorator(login_required)
    def post(self, request, meal_id_slug):
        """ Process the form submitted by the user """
        form = MealForm(request.POST, request.FILES)
        user = request.user

        if form.is_valid():
            if user:
                userprofile = user.userprofile
                meal = form.save(commit=False)
                meal.owner = userprofile
                meal.image = form.cleaned_data['image']
                meal.save()

                # Add many to many fields post save:

                # add tags from text
                tags = form.cleaned_data['tags']
                meal.tags.set(*tags)

                # add categories
                categories = form.cleaned_data['categories']
                meal.categories.set(categories)

                # automatically the user to the list of users who have this meal in their collection
                meal.users.add(userprofile)

                # Redirect to my_meals page
                return redirect(reverse('macro_mate:my_meals'))

        else:
            print(form.errors)
            return render(request, self.TEMPLATE, context={'form': form})
