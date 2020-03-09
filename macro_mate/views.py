from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from macro_mate.forms import UserForm, UserProfileForm, MealForm

# decorator
from django.contrib.auth.decorators import login_required

# JSON for cleaning meal input
import json


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
def add_meal(request):

    form = MealForm()

    if request.method == 'POST':
        form = MealForm(request.POST)

        # Get the user, no need to validate because @login_required
        user = request.user

        if form.is_valid():
            if user:
                page = form.save(commit=False)
                page.owner = user.userprofile
                page.save()  # See below comments

                # TAGIFY / TAGGIT "HACKS"
                # --------------------
                # Because of how Tagify.js adds values to inputs (rubbish software, change later...)
                # need to parse the json on the server.
                # https://github.com/yairEO/tagify/issues/197

                tag_json = json.loads(form['tags'].value())
                tag_list = [tag['value'] for tag in tag_json]

                # Save is done first because need primary key for many_many using taggit
                # https://github.com/jazzband/django-taggit/issues/527
                page.tags.set(*tag_list)

                # Redirect to meal viewer
                return redirect(reverse('macro_mate:index'))

        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'macro_mate/add_meal.html', context=context_dict)
