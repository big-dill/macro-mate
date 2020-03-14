from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from macro_mate.forms import UserForm, UserProfileForm, MealForm

from macro_mate.models import Meal, MealCategory
from taggit.models import Tag

# decorator
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


def meals(request):
    context_dict = {}
    response = render(request, 'macro_mate/meals.html', context=context_dict)
    return response


@login_required
def my_meals(request):
    context_dict = {}

    # get user, ensured via @login_required decorator
    user = request.user

    # get meals matching that user
    userprofile = user.userprofile
    meals = Meal.objects.filter(users=userprofile)

    # get meal categories
    def meal_by_cat(cat):
        return meals.filter(categories__category=cat).order_by('name')

    context_dict['categories'] = map(meal_by_cat, MealCategory.MEAL_CATEGORIES)

    # get the tags from those meals
    tag_set = set([])
    for meal in meals:
        tags = meal.tags.all()
        for tag in tags:
            tag_set.add(tag)

    context_dict['tags'] = list(tag_set)

    # get most recently added meals and same per category
    def most_recent(query_set):
        return query_set.order_by()[0:5]

    # get most recent 5 meals for each category
    context_dict['recent_categories'] = map(
        most_recent, context_dict['categories'])

    # press to see more
    context_dict['meals'] = meals

    response = render(request, 'macro_mate/my_meals.html',
                      context=context_dict)

    return response


@login_required
def add_meal(request):

    form = MealForm()

    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)

        # Get the user, no need to validate because @login_required
        user = request.user

        if form.is_valid():
            if user:
                userprofile = user.userprofile
                meal = form.save(commit=False)
                meal.owner = userprofile

                meal.image = form.cleaned_data['image']
                meal.save()  # save before adding tags to taggit

                # add tags from text
                # needed for custom form element from my understanding...
                tags = form.cleaned_data['tags']
                meal.tags.set(*tags)

                # add categories
                categories = form.cleaned_data['categories']
                meal.categories.set(categories)

                # automatically the user to the list of users who have this meal in their collection
                meal.users.add(userprofile)

                # Redirect to meal viewer
                return redirect(reverse('macro_mate:index'))

        else:
            print(form.errors)

    # Provide list of tags to the view
    context_dict = {'form': form}
    return render(request, 'macro_mate/add_meal.html', context=context_dict)
