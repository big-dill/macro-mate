from django.views import View
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


def index(request):
    context_dict = {}
    response = render(request, 'macro_mate/index.html', context=context_dict)
    return response


def user_login(request):
    # pulling the relevant login information
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        # if the login details are correct
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('macro_mate:index'))
            else:
                return HttpResponse("Your MacroMate account is disabled.")
        else:
            print("Incorrect login details: {username}, {password}")
            return HttpResponse("Incorrect login details")
    else:
        return render(request, 'macro_mate:login')


def register(request):
    registered = False

    # checking that the registration information is valid
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # updating the user object
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'macro_mate/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def meal(request):
    context_dict = {}
    response = render(request, 'macro_mate/meal.html', context=context_dict)
    return response


class AllMeals(View):
    """ A view for viewing all meals """

    TEMPLATE = 'macro_mate/all_meals.html'

    meals = Meal.objects.all()

    # Takes a context dict for subclasses to overwrite
    def get(self, request, context_dict={}, tag_slug=None):
        meals = self.meals

        try:
            tag = Tag.objects.get(slug=tag_slug)
            context_dict['tag'] = tag
            meals = meals.filter(tags__name__in=[tag.name])
            print(meals)
        except Tag.DoesNotExist:
            # Ignore modifying self.meals if no tags are found
            # Signal in context_dict so an error message can be displayed
            context_dict['tag-error'] = True
            pass

        self.set_meal_lists_with_recents(
            context_dict,
            'meals',
            meals
        )

        self.set_meal_lists_with_recents(
            context_dict,
            'breakfast',
            meals.filter(categories__category__in=MealCategory.BREAKFAST)
        )

        self.set_meal_lists_with_recents(
            context_dict,
            'lunch',
            meals.filter(categories__category__in=MealCategory.LUNCH)
        )

        self.set_meal_lists_with_recents(
            context_dict,
            'dinner',
            meals.filter(categories__category__in=MealCategory.DINNER)
        )

        self.set_meal_lists_with_recents(
            context_dict,
            'snack',
            meals.filter(categories__category__in=MealCategory.SNACK)
        )

        # get the tags from those meals
        tag_set = set([])
        for meal in meals:
            tags = meal.tags.all()
            for tag in tags:
                tag_set.add(tag)

        context_dict['tags'] = list(tag_set)

        return render(request, self.TEMPLATE, context=context_dict)

    def set_meal_lists_with_recents(self, context_dict, key, query_set):
        context_dict[key] = query_set
        context_dict["recent_" + key] = query_set.order_by('created_date')[0:5]


class MyMeals(AllMeals):
    """ A view for viewing the current logged in user's meals """

    @method_decorator(login_required)
    def get(self, request, tag_slug=None):
        # get user, ensured via @login_required decorator
        user = request.user
        # get meals matching that user
        userprofile = user.userprofile
        # Override meals to be those from a user
        self.meals = Meal.objects.filter(users=userprofile)
        # Override context dict to include user name
        self.context_dict = {
            'username': user.username,
            'user': user.id
        }

        print(user.username)
        # Call super get to run the usual get code
        return super().get(request, context_dict, tag_slug)


class AddMeal(View):
    """ A view for adding a meal to the database """

    @method_decorator(login_required)
    def get(self, request):
        """ Display the form for adding a meal """
        return render(request, 'macro_mate/add_meal.html', context={
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
