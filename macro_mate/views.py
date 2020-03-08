from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from macro_mate.models import User_Profile
from macro_mate.forms import UserForm, User_ProfileForm


# Create your views here.

def index(request):
    context_dict = {}
    response = render(request, 'macro_mate/index.html', context=context_dict)
    return response

def user_login(request):
    # pulling the relevant login information
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password = password)

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
        return render(request, 'macro_mate/index.html')

def register(request):
    registered = False

    # checking that the registration information is valid
    if request.method =='POST':
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

            profile.save

            registered = True;

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                'macro_mate/register.html',
                context = {'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered})




def meals(request):
    context_dict = {}
    response = render(request,  'macro_mate/meals.html', context=context_dict)
    return response
