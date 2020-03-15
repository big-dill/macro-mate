from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from macro_mate.forms import UserForm, UserProfileForm, MealForm

from macro_mate.models import Meal, MealCategory
from taggit.models import Tag

# decorator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    context_dict = {}
    response = render(request, 'macro_mate/index.html', context=context_dict)
    return response

# DO WE NEED THIS ANYMORE?
# May need to work on customising the login...

# def user_login(request):
#     # pulling the relevant login information
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)

#         # if the login details are correct
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('macro_mate:my_meals'))
#             else:
#                 return HttpResponse("Your MacroMate account is disabled.")
#         else:
#             print("Incorrect login details: {username}, {password}")
#             return HttpResponse("Incorrect login details")
#     else:
#         return render(request, 'macro_mate:login')


# def register(request):
#     registered = False

#     # checking that the registration information is valid
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()

#             # updating the user object
#             user.set_password(user.password)
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user

#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             profile.save()

#             registered = True

#         else:
#             print(user_form.errors, profile_form.errors)

#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()

#     return render(request,
#                   'macro_mate/register.html',
#                   context={'user_form': user_form,
#                            'profile_form': profile_form,
#                            'registered': registered})


def meal(request):
    context_dict = {}
    response = render(request, 'macro_mate/meal.html', context=context_dict)
    return response


class AllMeals(TemplateView):
    """ A view for viewing all meals """

    template_name = 'macro_mate/all_meals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        meals = Meal.objects.all()
        context['meals'] = meals

        tag_slug = self.kwargs.get('slug', None)

        if(tag_slug):
            try:
                tag = Tag.objects.get(slug=tag_slug)
                context['tag'] = tag
                meals = meals.filter(tags__name__in=[tag.name])
                print(meals)
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

        return context


class MyMeals(LoginRequiredMixin, AllMeals):
    """ A view for viewing the current logged in user's meals.
    Inherits from AllMeals and uses the LoginRequiredMixin to ensure that the user is logged in """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['meals'] = Meal.objects.filter(users=user.userprofile)
        context['username'] = user.username
        context['user_id'] = user.id
        return context


class AddMeal(View):
    """ A view for adding a meal to the database """

    TEMPLATE = "macro_mate/add_meal.html"

    @method_decorator(login_required)
    def get(self, request):
        """ Display the form for adding a meal """
        return render(request, self.TEMPLATE, context={
            'form': MealForm()
        })

    @method_decorator(login_required)
    def post(self, request):
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
